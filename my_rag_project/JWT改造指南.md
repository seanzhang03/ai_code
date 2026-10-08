# JWT 认证改造指南（FastAPI + Vue3）

> 本文档把「引入 JWT + bcrypt 密码哈希 + 接口鉴权 + 区分普通用户/管理员（角色权限）」的所有改动，按顺序、分文件整理出来，照着改即可。
> **本文档只做说明，不改动你的任何源码。** 每处改动都标注是「完整文件替换」还是「片段修改」，并给出改前 / 改后对照；所有代码片段都与当前项目真实代码一致。

---

## 0. 先弄懂要改什么、为什么

当前项目**其实没有真正的服务端认证**，存在四个问题：

| 问题 | 现状 | 改完后的效果 |
|---|---|---|
| 密码明文 | 密码明文存 MySQL，登录时 `password == results[0]["password"]` 直接比 | 全部 bcrypt 加盐哈希 |
| 接口裸奔 | 所有接口（含 admin、聊天、历史）任何人都能调 | 加 `Depends(get_current_user)`，没凭证一律 401 |
| 前端假登录 | 只在 `sessionStorage` 存个 `nickname`，控制台写个值就能绕过 | 登录签发 JWT，前端带 token，后端校验签名 |
| 无角色区分 | admin 接口任何登录用户都能调，前端也无限制 | admin 接口加 `token_check("admin")`，前端路由按角色拦截 |

改造思路：**bcrypt 哈希 + JWT 签发/校验 + 保护接口 + 前端带 token + `role` 字段区分 `'user'` 与 `'admin'`**。老用户密码用「懒迁移」处理——第一次登录成功后自动升级成哈希，不需跑额外脚本。

> 本次重构已确定两点：① 直接**修复并复用已有的 `common/JWTUtil.py`**（不另建 `security.py`）；② **前后端双重**控制管理员权限（后端 403 兜底 + 前端路由守卫拦截）。

---

## 1. 涉及文件清单

| 文件 | 改动性质 |
|---|---|
| MySQL `users` 表 | 加 `role` 字段（1 条 ALTER + 标记管理员） |
| `.env` | **核对**（已有 JWT 配置，仅建议调整过期时间） |
| `common/JWTUtil.py` | **完整文件替换**（修复全部 bug） |
| `registration/service/RegistrationService.py` | 片段：存哈希 |
| `registration/dao/RegistrationDao.py` | 片段：入库带默认角色 |
| `login/dao/LoginDao.py` | 片段：新增一个函数 |
| `login/service/LoginService.py` | 片段：校验 + 签发含 role 的 token + 懒迁移 |
| `password/service/PasswordService.py` | 片段：校验/哈希 + 修一个语法 bug |
| `admin/dao/AdminDao.py` | 片段：默认密码哈希 + 建用户带默认角色 |
| `chat/controller/ChatController.py` | 片段：加鉴权 |
| `history/controller/HistoryController.py` | **完整文件替换**（加鉴权 + 修 IDOR） |
| `admin/controller/AdminController.py` | 片段：加管理员角色校验 |
| `password/controller/PasswordController.py` | 片段：仅「凭旧密码改密」加鉴权 |
| `my-vue-app/src/main.js` | 片段：拦截器 + 守卫改判 token/角色 |
| `my-vue-app/src/router/index.js` | 片段：`/admin` 加 `requiresAdmin` |
| `my-vue-app/src/components/Login.vue` | 片段：三处存 token + 修验证码登录 bug |
| `my-vue-app/src/components/Chat.vue` | 片段：SSE 带 token、补退出登录、按角色显隐管理入口 |

---

## 2. 开始改

### 第 0 步：安装依赖

```bash
pip install python-jose bcrypt
```

> 项目里已 `import` 了 `python-jose`、`bcrypt`，多数情况下已装好；跑一遍确保齐全即可。HS256 用不到 cryptography 后端，以后换 RS256 再装 `python-jose[cryptography]`。
> 旧的 `JWTUtil.py` 用到了 `passlib`，本次重写后改用 `bcrypt` 直用，`passlib` 可留着也可删。

---

### 第 1 步：`.env` 核对（无需新增）

你的 `.env` 末尾**已经**有 JWT 配置了（旧指南误以为要新加），内容如下：

```
#JWT认证
SECRET_KEY=EchYWOEVCJWYpXXVpIBCwu-pRjWLanjH5biscPtu-aI
ALGORITHM=HS256 #算法名称
ACCESS_TOKEN_EXPIRE_MINUTES=10 #token过期事件[分钟]
```

只需做两件事：

1. **把过期时间调大**：`ACCESS_TOKEN_EXPIRE_MINUTES=10` 表示 token 10 分钟就失效，开发调试会频繁掉线，建议改成 `1440`（1 天）。
2. **换一个强 `SECRET_KEY`**：当前值是明示的占位串，建议换成你自己的随机长串（比如 `openssl rand -hex 32` 生成的结果）。不加引号也能读，但建议写成 `SECRET_KEY=你的一长串随机字符`。

> 代码里用 `int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))` 读取，会自动转整数，所以这里写纯数字即可。

---

### 第 2 步：重写 `common/JWTUtil.py`（**完整文件替换**）

原文件已存在但有多处 bug 且从未被业务调用，直接整体替换。修掉的 bug：`HTTPException` 来源错误（原来是 aiohttp 的）、`algorithm` 环境变量大小写不一致、`timedelta(minutes=str)` 类型错误、`verify_token` 用 `return` 而非 `raise`、`token_check` 重复代码且用 `roleName` 混搭。

```python
'''
    JWT 相关工具：密码哈希、token 签发/校验、获取当前登录用户、角色鉴权依赖
'''
import os
from datetime import datetime, timedelta, timezone

import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, Header, HTTPException, Query
from jose import JWTError, jwt

load_dotenv()

# 启动时只读一次环境变量，避免每次调用都重复解析
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))


def hash_password(plain: str) -> str:
    """对明文密码进行 bcrypt 加盐哈希，返回可入库的字符串。"""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """校验明文密码与库中哈希是否匹配。"""
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def create_token(data: dict) -> str:
    """根据载荷 dict 签发 JWT，自动写入过期时间(exp)与签发时间(iat)。"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """校验 JWT，成功返回载荷；失败抛出 401。"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        # jose 里"过期"(ExpiredSignatureError)是 JWTError 的子类，一个 except 全兜住
        raise HTTPException(status_code=401, detail="登录凭证无效或已过期")


def get_current_user(
    authorization: str = Header(default=None),
    token: str = Query(default=None),
) -> dict:
    """FastAPI 依赖：从 Authorization 头(标准)或 ?token= 查询参数(SSE 场景)解析当前用户。

    说明：SSE(EventSource) 无法自定义请求头，聊天接口允许通过 ?token= 传令牌，
    所以这里同时支持两种取令牌方式。
    """
    raw = None
    if authorization and authorization.startswith("Bearer "):
        raw = authorization[7:]
    elif token:
        raw = token
    if not raw:
        raise HTTPException(status_code=401, detail="未登录")

    payload = verify_token(raw)
    return {
        "user_id": int(payload.get("sub")),
        "nickname": payload.get("nickname"),
        "role": payload.get("role"),
    }


def token_check(required_role: str):
    """返回一个依赖：要求当前用户 role == required_role，否则 403。

    用法：Depends(token_check("admin")) —— 只有管理员角色能通过。
    """
    def check_role(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") != required_role:
            raise HTTPException(status_code=403, detail="无权限执行该操作")
        return current_user
    return check_role
```

---

### ⚠️ 数据库迁移：给 `users` 表加 `role` 字段（改第 4、5、7 步前先做）

`users` 表目前没有角色字段，先加一列：

```sql
-- 1) 加角色字段，默认普通用户
ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'user';

-- 2) 把某个邮箱指定为管理员（把邮箱换成你自己的）
UPDATE users SET role='admin' WHERE email='你的管理员邮箱@qq.com';
```

> 跑完第 1 条，所有已有用户都变 `'user'`；再用第 2 条把你自己的邮箱提成 `'admin'`。以后想再设管理员，重复第 2 条即可。

---

### 第 3 步：注册时存哈希 + 默认角色（共 2 个文件）

**① `registration/service/RegistrationService.py`：存哈希**

在顶部 `from common.JudgeEmail import judge_email`（第 7 行）下面加导入：

```python
from common.JWTUtil import hash_password
```

改这一行（第 26 行）：

```python
# 改前
                save_registration_result(email,password,nickname)
# 改后
                save_registration_result(email, hash_password(password), nickname)
```

**② `registration/dao/RegistrationDao.py`：SQL 带默认角色 `'user'`**

```python
# 改前
        sql = "INSERT INTO users VALUES(NULL,%s,%s,%s,now())"
        cursor.execute(sql,[
            email,
            password,
            nickname,
            ])
# 改后（用显式列名，并固定 role='user' 作为普通用户默认角色）
        sql = "INSERT INTO users (email,password,nickname,role) VALUES(%s,%s,%s,'user')"
        cursor.execute(sql,[
            email,
            password,
            nickname,
            ])
```

---

### 第 4 步：`login/dao/LoginDao.py`（片段：新增一个函数）

在文件末尾、`if __name__ == "__main__"` 这段**之前**，加：

```python
#根据邮箱更新密码（用于存量明文密码的“懒迁移”）
def update_password_by_email(email, hashed_password):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    try:
        sql = "UPDATE users SET password=%s WHERE email=%s"
        cursor.execute(sql, [hashed_password, email])
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        LoadMySQLConn.close_mysql_conn(cursor, conn)
```

---

### 第 5 步：`login/service/LoginService.py`（片段，共 5 处）

**① 顶部 `import smtplib` 下面加导入**：

```python
from common.JWTUtil import hash_password, verify_password, create_token
```

**② `load_dotenv()` 之后、`send_captcha` 函数之前，加一个辅助函数**：

```python
#密码校验 + 懒迁移：存量密码是明文，登录成功后自动升级为 bcrypt 哈希
def _verify_and_upgrade(plain_password, stored_password, email):
    if stored_password.startswith(("$2a$", "$2b$", "$2y$")):
        #已经是 bcrypt 哈希
        return verify_password(plain_password, stored_password)
    #旧明文密码：直接比较，成功后升级为哈希
    if plain_password == stored_password:
        LoginDao.update_password_by_email(email, hash_password(plain_password))
        return True
    return False
```

**③ `login_by_email_captcha`：把整个函数替换**（原来验证码通过后只回 `data:None`，没返回任何用户信息，这是要修的 bug）：

```python
#通过邮箱和验证码登录
def login_by_email_captcha(email, captcha):
    redis_conn = LoadRedisConn().conn
    redis_captcha = redis_conn.get(email)
    if not redis_captcha:
        return {
            "code":500,
            "msg":"验证码已过期",
            "data":None
        }
    if redis_captcha == captcha:
        #验证码通过后，查询用户信息并签发 token
        results = LoginDao.query_users_by_email(email)
        if len(results) == 0:
            return {"code":500, "msg":"邮箱未注册", "data":None}
        token = create_token({"sub": str(results[0]["users_id"]), "nickname": results[0]["nickname"], "role": results[0]["role"]})
        return {
            "code":200,
            "msg":"登录成功",
            "data":{
                "access_token": token,
                "nickname": results[0]["nickname"],
                "usersId": results[0]["users_id"],
                "role": results[0]["role"]
            }
        }
    return {
        "code":500,
        "msg":"验证码错误",
        "data":None
    }
```

**④ `login_by_email_password` 的 `else` 分支整体替换**：

```python
    else:
        if _verify_and_upgrade(password, results[0]["password"], email):
            token = create_token({"sub": str(results[0]["users_id"]), "nickname": results[0]["nickname"], "role": results[0]["role"]})
            print("登录成功!")
            return {
                "code":200,
                "msg":"登录成功",
                "data":{
                    "access_token": token,
                    "nickname": results[0]["nickname"],
                    "usersId": results[0]["users_id"],
                    "role": results[0]["role"]
                }
            }
        else:
            print("密码错误！请重新登陆。")
            return {
                "code":500,
                "msg":"密码错误",
                "data":None
            }
```

**⑤ `login_by_nickname_password` 的 `else` 分支整体替换**：

```python
    else:
        if _verify_and_upgrade(password, results[0]["password"], results[0]["email"]):
            token = create_token({"sub": str(results[0]["users_id"]), "nickname": results[0]["nickname"], "role": results[0]["role"]})
            print("登录成功!")
            return {
                "code": 200,
                "msg": "登录成功",
                "data": {
                    "access_token": token,
                    "nickname": results[0]["nickname"],
                    "usersId": results[0]["users_id"],
                    "role": results[0]["role"]
                }
            }
        else:
            print("密码错误！请重新登陆。")
            return {
                "code": 500,
                "msg": "密码错误",
                "data": None
            }
```

> 说明：
> - ⑤ 处原来函数参数里没有 `email`，`query_users_by_nickname` 是 `SELECT *`，所以懒迁移用 `results[0]["email"]` 取那一行的邮箱来升级密码。
> - 三处 `create_token` 都带上 `"role": results[0]["role"]`，且 `data` 里也回传 `role`，前端会拿来判断是否是管理员。

---

### 第 6 步：`password/service/PasswordService.py`（片段，共 4 处）

**① 顶部 `from password.dao.PasswordDao import query_users_by_email,change_password` 下面加导入**：

```python
from common.JWTUtil import hash_password, verify_password
```

**② `change_password_by_password` 里这两行（第 77、79 行附近）**：

```python
        # 改前
        if old_password== results[0]["password"]:
            print("密码正确，下面开始修改密码")
            change_password(email,new_password)
        # 改后
        if verify_password(old_password, results[0]["password"]) or old_password == results[0]["password"]:
            print("密码正确，下面开始修改密码")
            change_password(email, hash_password(new_password))
```

> `or old_password == results[0]["password"]` 是为了兼容还没升级的老用户（旧密码仍是明文），升级成哈希后就只走 `verify_password` 了。

**③ `change_password_by_captcha` 里这一行**：

```python
        # 改前
        change_password(email,new_password)
        # 改后
        change_password(email, hash_password(new_password))
```

**④ 顺带修一个现有语法 bug**：`change_password_by_captcha` 里返回的字典少了逗号，且 `data:None` 少了引号，改成：

```python
        # 改前（会报错：字典里少逗号，"data:None" 应为 "data":None）
        return {
            "code":200,
            "msg":"修改密码成功"
            "data:None"
        }
        # 改后
        return {
            "code":200,
            "msg":"修改密码成功",
            "data":None
        }
```

---

### 第 7 步：`admin/dao/AdminDao.py`（片段，共 3 处）

**① 顶部加导入**：

```python
from common.JWTUtil import hash_password
```

**② `create_users_with_email_nickname`：换哈希 + 带默认角色 `'user'`**：

```python
        # 改前
        sql = "INSERT INTO users VALUES(NULL,%s,%s,%s,now())"
        cursor.execute(sql,[
            email,
            "123456",
            nickname,
        ])
        # 改后（用显式列名，并固定 role='user'）
        sql = "INSERT INTO users (email,password,nickname,role) VALUES(%s,%s,%s,'user')"
        cursor.execute(sql,[
            email,
            hash_password("123456"),
            nickname,
        ])
```

**③ `password_init_by_nickname` 里**：

```python
        # 改前
        sql = "UPDATE users SET password='123456' WHERE nickname=%s;"
        cursor.execute(sql,[name])
        # 改后
        sql = "UPDATE users SET password=%s WHERE nickname=%s"
        cursor.execute(sql,[hash_password("123456"), name])
```

---

### 第 8 步：四个控制器加鉴权

#### `chat/controller/ChatController.py`（片段）

```python
# 改前 top 两行
from fastapi import APIRouter
...
chat_router = APIRouter()
# 改后
from fastapi import APIRouter, Depends
from common.JWTUtil import get_current_user
...
chat_router = APIRouter(dependencies=[Depends(get_current_user)])
```

> 因为 `get_current_user` 声明了 `token: str = Query(default=None)`，前端 `/chat/chat?...&token=xxx` 里的 `token` 会作为查询参数被自动识别，无需改 `chat(question, historyId)` 的签名。

#### `history/controller/HistoryController.py`（**完整文件替换**）

除加鉴权外，顺带修掉 IDOR（越权）：原来任何人都能传任意 `usersId`/`userId` 查别人历史，现在统一用登录用户自己的 id。

```python
'''
    操作历史记录的路由
'''
from fastapi import APIRouter, Depends
from common.JWTUtil import get_current_user
from history.service import HistoryService
from history.entity.HistoryEntity import SaveChatResultsEntity

history_router = APIRouter(dependencies=[Depends(get_current_user)])

#根据用户id来显示该用户所有对话窗口历史记录
@history_router.get("/queryHistoryMenu/{usersId}")
def query_history_menu(usersId:int, current_user:dict=Depends(get_current_user)):
    #IDOR修复：忽略URL里的usersId，改用登录用户自己的id
    return HistoryService.query_history_menu(current_user["user_id"])

#根据历史id查询某个窗口完整的上下文记录和其所有子记录
@history_router.get("/queryHistoryList/{historyId}")
def query_history_list(historyId:str):
    return HistoryService.query_history_list(historyId)

#保存对话记录
@history_router.post("/saveChatResult")
def save_chat_result(save_chat_results_entity:SaveChatResultsEntity, current_user:dict=Depends(get_current_user)):
    #IDOR修复：忽略body里的userId，改用登录用户自己的id
    return HistoryService.save_chat_result(
        current_user["user_id"],
        save_chat_results_entity.question,
        save_chat_results_entity.answer,
        int(save_chat_results_entity.parentId)
        )
```

#### `admin/controller/AdminController.py`（片段）

```python
# 改前 top 两行 + router 定义
from fastapi import APIRouter
...
admin_router = APIRouter()
# 改后
from fastapi import APIRouter, Depends
from common.JWTUtil import token_check
...
# 用 token_check("admin") 替代 get_current_user：只有管理员角色能调，普通用户 403
admin_router = APIRouter(dependencies=[Depends(token_check("admin"))])
```

#### `password/controller/PasswordController.py`（片段，**只锁一个接口**）

> 注意：**不要**像旧指南那样把整个 password 路由都挂 `get_current_user`，否则会锁死「验证码找回/改密」流程（忘记密码的人没法登录去改密）。只有「凭旧密码改密」这个接口需要登录。

```python
# 改前 top 两行
from fastapi import APIRouter
from password.service import PasswordService
from password.entity.PasswordEntity import ChangePasswordCaptchaEntity,ChangePasswordPasswordEntity
password_router = APIRouter()
# 改后（只加 Depends 与导入）
from fastapi import APIRouter, Depends
from common.JWTUtil import get_current_user
from password.service import PasswordService
from password.entity.PasswordEntity import ChangePasswordCaptchaEntity,ChangePasswordPasswordEntity
password_router = APIRouter()

# 仅这个接口加 current_user 依赖；sendCaptcha、changePasswordCaptcha 保持公开
@password_router.post("/changePasswordPassword")
def change_password_by_password(change_password_password_entity:ChangePasswordPasswordEntity, current_user:dict=Depends(get_current_user)):
    return PasswordService.change_password_by_password(
        change_password_password_entity.email,
        change_password_password_entity.old_password,
        change_password_password_entity.new_password
        )
```

---

### 第 9 步：前端 `my-vue-app/src/main.js`（片段，共 2 处）

**① 在 `app.config.globalProperties.$axios = axios` 这行后面，加两个拦截器**：

```js
//请求拦截器：自动携带 token
axios.interceptors.request.use(config => {
  const token = sessionStorage.getItem("access_token")
  if (token) {
    config.headers["Authorization"] = "Bearer " + token
  }
  return config
})

//响应拦截器：401 时清空会话并跳回登录页
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      sessionStorage.clear()
      router.push("/login")
    }
    return Promise.reject(error)
  }
)
```

**② 把导航守卫整体替换**（原来只判 `nickname`，改成判 `access_token`，并对管理员页额外判 `role`）：

```js
router.beforeEach((to,from,next)=>{
  if(to.meta.isLogin){
    const token = sessionStorage.getItem("access_token")
    if(token===null || token.length===0){
      next("/login")
      return
    }
    //管理员页面额外校验角色：只有 role==='admin' 才能进
    if(to.meta.requiresAdmin){
      if(sessionStorage.getItem("role")==="admin"){
        next()
      }else{
        next("/chat")  //普通用户无权限，跳回聊天页
      }
    }else{
      next()
    }
  }else{
    next()
  }
})
```

---

### 第 10 步：前端 `my-vue-app/src/router/index.js`（片段）

给 `/admin` 路由的 meta 里加 `requiresAdmin: true`：

```js
        //管理员路由配置
        {
            path:"/admin",
            meta:{
                isLogin:true,
                requiresAdmin:true,   //新增：仅管理员可进
            },
            component:()=>import("../components/Admin.vue")
        },
```

---

### 第 11 步：前端 `my-vue-app/src/components/Login.vue`（片段，共 3 处）

三个登录成功的地方，都要存 `access_token` 和 `role`。后端已在这些接口的 `data` 里返回了这两个字段。

**① `loginByEmailCaptcha` 的 `if(res.data.code ===200)` 块里，`alert("登录成功！")` 后加**（顺带修掉原来验证码登录不存用户信息的 bug）：

```js
      sessionStorage.setItem("access_token",res.data.data.access_token)
      sessionStorage.setItem("role",res.data.data.role)
      sessionStorage.setItem("nickname",res.data.data.nickname)
      sessionStorage.setItem("usersId",res.data.data.usersId)
```

**② `loginByEmailPassword` 的 `if(res.data.code ===200)` 块里，`sessionStorage.setItem("usersId",...)` 那行后加**：

```js
      sessionStorage.setItem("access_token",res.data.data.access_token)
      sessionStorage.setItem("role",res.data.data.role)
```

**③ `loginByNicknamePassword` 的 `if(res.data.code ===200)` 块里，同样加**：

```js
      sessionStorage.setItem("access_token",res.data.data.access_token)
      sessionStorage.setItem("role",res.data.data.role)
```

---

### 第 12 步：前端 `my-vue-app/src/components/Chat.vue`（片段，共 4 处）

**① SSE 请求带上 token（第 153 行）**：

```js
// 改前
let sse = new EventSource("http://localhost:8000/chat/chat?"+params)
// 改后
let sse = new EventSource("http://localhost:8000/chat/chat?"+params+"&token="+sessionStorage.getItem("access_token"))
```

**② 顶部补 `useRouter` 导入 + 定义 `router`**（当前 Chat.vue 没有引入路由，导致 `logout()` 无法跳转）：

```js
// 改前
import {ref, watch,computed,getCurrentInstance, onMounted,nextTick} from "vue";
// 改后（加一行引入 useRouter）
import {ref, watch,computed,getCurrentInstance, onMounted,nextTick} from "vue";
import {useRouter} from "vue-router"

// 在 let proxy = getCurrentInstance().proxy 附近，补一行
let router = useRouter()
```

**③ 补 `logout()` 实现 + 按角色显隐管理入口**：

先加一个 `role` 变量（用于控制管理入口显隐），并在 `onMounted` 里赋值：

```js
let role = ref("user")
```

在 `onMounted(()=>{ ... })` 里，`nickname.value = ...` 那行后加：

```js
  role.value = sessionStorage.getItem("role") || "user"
```

然后把模板里用户菜单的 `<select>` 加一个管理员选项（第 30–34 行）：

```html
        <select @change = 'handleUserCommand($event.target.value)'>
          <option value="profile">个人中心</option>
          <option value="settings">设置</option>
          <option v-if="role==='admin'" value="admin">管理后台</option>
          <option value="logout">退出登录</option>
        </select>
```

在 `handleUserCommand` 里补 `admin` 分支，并定义 `logout()`：

```js
function handleUserCommand(command){
  switch(command){
    case "profile":
      ElMessage.info("个人中心功能开发中")
      break
    case "settings":
      ElMessage.info("设置功能开发中")
      break
    case "admin":
      router.push("/admin")
      break
    case "logout":
      logout()
      break
  }
}

//退出登录：清空会话并回登录页
function logout(){
  sessionStorage.clear()
  router.push("/login")
}
```

> 顺带提醒（非 JWT 必需，可自行决定）：Chat.vue 里 `ElMessage` 没 import（历史遗留），点上面的菜单会报错；如需使用，在顶部加 `import { ElMessage } from "element-plus"`。

**④ `saveChatResult` / `queryHistoryMenu`（可不动）**：这两个仍然向前端传 `usersId`，但后端已改成用登录用户自己的 id（见第 8 步 IDOR 修复），所以传什么都会被忽略，无需修改。

---

### 第 13 步：前端 `my-vue-app/src/components/Admin.vue`

**无需改动。** 入口已被第 10 步的路由守卫（`requiresAdmin`）和第 12 步的菜单显隐控制住，后端第 8 步又用 `token_check("admin")` 兜底 403，三重保障。

---

## 3. 改完怎么验证

1. 先执行数据库迁移（第「⚠️数据库迁移」那 2 条 SQL），`SELECT ... FROM users` 确认多了 `role` 列。
2. 重启后端 `uvicorn main:app`；重启前端 `npm run dev`。
3. 新注册一个用户 → 查 MySQL，`password` 应是 `$2b$...` 开头的哈希，`role` 默认 `'user'`。
4. 老用户（仍是明文密码）登录一次 → 登录成功，且该行密码被自动升级成哈希（懒迁移生效）。
5. 不登录直接浏览器访问 `/chat` → 被重定向回 `/login`（前端拦截 + 后端 401）。
6. 登录后正常聊天 → 流式输出正常（token 通过 `?token=` 传给了 SSE）。
7. 用 A 账号登录，请求 `history/queryHistoryMenu/{别的id}` → 仍只返回 A 自己的历史（IDOR 已封）。
8. 未登录直接 `curl` 调 `admin/deleteUsers` → 401。
9. 普通用户（role='user'）登录后调 `admin/deleteUsers` → 403；前端访问 `/admin` 被守卫拦回 `/chat`。
10. 管理员（role='admin'）登录后调 `admin/deleteUsers` → 200，且聊天页菜单里出现「管理后台」。
11. 回归验证：未登录也能走「验证码找回/改密」流程（`sendCaptcha` + `changePasswordCaptcha` 仍公开可用）。

---

## 4. 注意事项 & 暂缓项

- **懒迁移**替代一次性迁移脚本：老用户第一次登录成功后，旧明文密码自动变哈希，无需单独跑脚本。
- **角色区分**：`users` 表 `role` 字段决定身份（'user'/'admin'），登录时把角色写进 JWT，admin 接口用 `token_check("admin")` 校验，前端路由用 `requiresAdmin` 校验。设管理员就执行 `UPDATE users SET role='admin' WHERE email='...'`。
- **SSE 鉴权**：`EventSource` 无法带请求头，所以 `get_current_user` 额外支持 `?token=`，Chat.vue 把 token 拼在 URL 上。
- **暂缓项**（本期没做，需要时可再补）：
  - `queryHistoryList/{historyId}` 仍能靠猜 historyId 读任意记录（所有权校验暂缓）。
  - 未做 refresh token、登出踢人（Redis 黑名单）、HTTPS 强制。
  - 前端仍冗余存储/传 `usersId`（后端已忽略，纯属遗留可清理）。
  - 备份前端 `未增加样式的客户端文件/` 不在本期范围；若也要跑，把第 9–12 步照搬过去即可。