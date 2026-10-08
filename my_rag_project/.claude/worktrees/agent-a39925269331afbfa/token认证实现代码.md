# Token 认证实现代码（FastAPI + Vue3）

> 本文档是你项目的 **Token(JWT) 认证改造** 的**完整代码交付**：每个被改文件的**最终完整内容**都写在下面，可直接整文件覆盖粘贴。
> 全程**不修改任何源码**，只做这一步：把下面每个文件的代码复制覆盖到对应路径即可。
>
> 已确认的方案：
> - 密码改为 **bcrypt 哈希**（老明文用户首次登录成功后自动升级 = 懒迁移）。
> - 角色用**独立的 `role` 表**（列：`users_id`、`role`，role 取值 `'admin'` / `'user'`），**不是**在 `users` 表加列。

---

## 零、先装依赖（如未装）

```bash
pip install python-jose bcrypt
```

> HS256 用不到 cryptography，`python-jose` 即可；以后换 RS256 再 `pip install python-jose[cryptography]`。

---

## 一、数据库（先执行这一步）

`role` 表结构（你已建表的话只需保证两列名一致即可）：

```sql
-- 参考 DDL（若你的表结构不同，仅需保证列名与取值一致）
CREATE TABLE `role` (
  `users_id` INT NOT NULL,
  `role`     VARCHAR(20) NOT NULL DEFAULT 'user',
  PRIMARY KEY (`users_id`)
);
```

把某个用户设为管理员（自动「有则更新、无则插入」）：

```sql
INSERT INTO `role` (users_id, role)
VALUES ((SELECT users_id FROM users WHERE email='你的管理员邮箱@qq.com'), 'admin')
ON DUPLICATE KEY UPDATE role='admin';
```

> 若你的 `role` 表 `users_id` 没设主键/唯一键，则分两步：
> ```sql
> UPDATE `role` SET role='admin' WHERE users_id=(SELECT users_id FROM users WHERE email='你的管理员邮箱@qq.com');
> -- 若上面影响 0 行，再执行：
> INSERT INTO `role` (users_id, role) VALUES ((SELECT users_id FROM users WHERE email='你的管理员邮箱@qq.com'), 'admin');
> ```

---

## 二、后端完整代码（11 个文件）

### 1. `common/JWTUtil.py`（**整文件替换**）

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
        # jose 里"过期"(ExpiredSignatureError) 是 JWTError 的子类，一个 except 全兜住
        raise HTTPException(status_code=401, detail="登录凭证无效或已过期")


def get_current_user(
    authorization: str = Header(default=None),
    token: str = Query(default=None),
) -> dict:
    """FastAPI 依赖：从 Authorization 头(标准) 或 ?token= 查询参数(SSE 场景) 解析当前用户。

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
        "role": payload.get("role", "user"),
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

### 2. `login/dao/LoginDao.py`（**整文件替换**，新增 2 个函数）

```python
'''
该模块实现针对于登录模块操作数据库的操作
'''
from common.LoadMySQLConn import LoadMySQLConn

#根据用户邮箱查询用户信息
def query_users_by_email(email):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE email=%s"
    cursor.execute(sql,[email])
    results = cursor.fetchall()
    LoadMySQLConn.close_mysql_conn(cursor,conn)
    return results

#根据用户名称查询用户信息
def query_users_by_nickname(name):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE nickname=%s"
    cursor.execute(sql,[name])
    results = cursor.fetchall()
    LoadMySQLConn.close_mysql_conn(cursor,conn)
    return results

#根据用户id查询其角色（role 表；无记录由调用方按 'user' 兜底）
def query_role_by_user_id(users_id):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    sql = "SELECT role FROM `role` WHERE users_id=%s"
    cursor.execute(sql,[users_id])
    results = cursor.fetchall()
    LoadMySQLConn.close_mysql_conn(cursor,conn)
    return results

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

if __name__ == "__main__":
    print(query_users_by_email("2012761893@qq.com"))
```

---

### 3. `login/service/LoginService.py`（**整文件替换**）

```python
'''
    本模块实现用户的登录和通过验证码,若用户没有注册，则跳转到注册界面
'''
import os

from login.dao import LoginDao
from dotenv import load_dotenv
from login.utils.CreateCaptchaUtil import CreateCaptchaUtil
from email.mime.text import MIMEText
from common.LoadRedisConn import LoadRedisConn
from common.JWTUtil import hash_password, verify_password, create_token
import smtplib

load_dotenv()

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

#查询用户角色；role 表里无记录时默认普通用户
def _get_role(users_id):
    rows = LoginDao.query_role_by_user_id(users_id)
    return rows[0]["role"] if rows else "user"

def send_captcha(email):
    #1.通过邮箱获取到对应数据
    results = LoginDao.query_users_by_email(email)
    #2.根据查询结果判定是否有登录条件，若未注册，返回信息并跳转到对应注册页面
    if len(results) == 0:
        print("该邮箱未注册")
        return {
            "code":500,
            "msg":"邮箱未注册",
            "data":None
        }
    #3.创建邮件对象的相关信息
    #发件人信息
    send_email=os.getenv("SEND_EMAIL")
    #授权码信息
    auth_code = os.getenv("AUTH_CODE")
    #邮件主题
    subject = "您正在通过邮箱进行影视问答系统的登录"
    #实例化对象并调用
    create_captcha_util = CreateCaptchaUtil()
    captcha = create_captcha_util.captcha
    print(captcha)
    content =f"你本次登录的验证码为{captcha}，过期时间为5分钟"
    messages = MIMEText(content,"plain","utf-8")
    messages["From"] = send_email
    messages["To"] = email
    messages["Subject"] = subject
    #4.连接qq邮箱服务器
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp = smtplib.SMTP(smtp_server,smtp_port)
    smtp.starttls()
    smtp.login(send_email,auth_code)
    smtp.sendmail(send_email,email,messages.as_string())
    smtp.quit()
    #5.将验证码放到redis中
    try:
        redis_conn = LoadRedisConn.load_redis_conn()
        redis_conn.setex(email,300,captcha)
        LoadRedisConn.close_redis_conn(redis_conn)
        print("验证码已经发送！")
        return{
            "code":200,
            "msg":"验证码已发送",
            "data":{
                "nickname":results[0]["nickname"],
                "usersId":results[0]["users_id"]
            }
        }
    except Exception as e:
        print(f"验证码发送失败！具体原因：{e}")
        return{
            "code":500,
            "msg":"验证码发送失败",
            "data":None
        }

#通过邮箱和验证码登录
def login_by_email_captcha(email, captcha):
    redis_conn = LoadRedisConn().conn
    redis_captcha = redis_conn.get(email)
    if not redis_captcha:
        return{
            "code":500,
            "msg":"验证码已过期",
            "data":None
        }
    if redis_captcha == captcha:
        #验证码通过后，查询用户信息并签发 token
        results = LoginDao.query_users_by_email(email)
        if len(results) == 0:
            return {"code":500, "msg":"邮箱未注册", "data":None}
        role = _get_role(results[0]["users_id"])
        token = create_token({"sub": str(results[0]["users_id"]), "nickname": results[0]["nickname"], "role": role})
        return {
            "code":200,
            "msg":"登录成功",
            "data":{
                "access_token": token,
                "nickname": results[0]["nickname"],
                "usersId": results[0]["users_id"],
                "role": role
            }
        }
    return {
        "code":500,
        "msg":"验证码错误",
        "data":None
    }

#通过邮箱和保存的密码登录
def login_by_email_password(email:str, password:str):
    results = LoginDao.query_users_by_email(email)
    if len(results) == 0:
        print("您输入的邮箱未注册！")
        return {
            "code":500,
            "msg":"邮箱未注册",
            "data":None
        }
    if _verify_and_upgrade(password, results[0]["password"], email):
        print("登录成功!")
        role = _get_role(results[0]["users_id"])
        token = create_token({"sub": str(results[0]["users_id"]), "nickname": results[0]["nickname"], "role": role})
        return {
            "code":200,
            "msg":"登录成功",
            "data":{
                "access_token": token,
                "nickname": results[0]["nickname"],
                "usersId": results[0]["users_id"],
                "role": role
            }
        }
    print("密码错误！请重新登陆。")
    return {
        "code":500,
        "msg":"密码错误",
        "data":None
    }

#通过用户名和保存的密码登录
def login_by_nickname_password(nickname:str, password:str):
    results = LoginDao.query_users_by_nickname(nickname)
    if len(results) == 0:
        print("您输入的用户名未注册！")
        return {
            "code": 500,
            "msg": "用户名未注册",
            "data": None
        }
    if _verify_and_upgrade(password, results[0]["password"], results[0]["email"]):
        print("登录成功!")
        role = _get_role(results[0]["users_id"])
        token = create_token({"sub": str(results[0]["users_id"]), "nickname": results[0]["nickname"], "role": role})
        return {
            "code": 200,
            "msg": "登录成功",
            "data": {
                "access_token": token,
                "nickname": results[0]["nickname"],
                "usersId": results[0]["users_id"],
                "role": role
            }
        }
    print("密码错误！请重新登陆。")
    return {
        "code": 500,
        "msg": "密码错误",
        "data": None
    }
```

---

### 4. `registration/service/RegistrationService.py`（**整文件替换**）

```python
'''
    该模块是实现用户注册功能的部分
'''
from registration.dao.RegistrationDao import save_registration_result
from login.dao.LoginDao import query_users_by_email,query_users_by_nickname
from pydantic import Field,BaseModel
from common.JudgeEmail import judge_email
from common.JWTUtil import hash_password

#用户注册
def registration(email:str,password:str,nickname:str):
    #查询该邮件是否注册
    email_results = query_users_by_email(email)
    nickname_results = query_users_by_nickname(nickname)
    print()
    #邮箱未注册则进行注册功能
    if len(email_results) == 0 and len(nickname_results)==0:
        if judge_email(email) == False:
            print("邮箱格式不正确！请重新输入")
            return {
                "code":500,
                "msg":"邮箱格式不正确",
                "data":None
            }
        elif judge_email(email) == True:
            try:
                #数据库入库操作（密码哈希后再入库）
                save_registration_result(email, hash_password(password), nickname)
                email_rs = query_users_by_email(email)
                nickname_rs = query_users_by_nickname(nickname)
                if len(email_rs) != 0 and len(nickname_rs)!=0:
                    print("注册成功")
                    return{
                        "code":200,
                        "msg":"注册成功",
                        "data":None
                    }
            except Exception as e:
                print(f"注册失败:{e}")
                return {
                    "code":500,
                    "msg":"注册失败，请重新注册",
                    "data":None,
                }
    #邮箱已注册则拒绝注册
    else :
        print("该邮箱或用户名已经注册！请回到登录页面直接登录。")
        return {
            "code":500,
            "msg":"该邮箱或用户名已经注册",
            "data":None
        }

if __name__ == "__main__":
    registration(email="123456@qq.com",nickname="dds",password="123456")
```

---

### 5. `registration/dao/RegistrationDao.py`（**整文件替换**）

```python
'''
    该模块是将未注册的用户进行注册时，操作数据库的具体代码
'''
from common.LoadMySQLConn import LoadMySQLConn

#保存用户注册信息（同时写入默认角色 'user'）
def save_registration_result(email:str,password:str,nickname:str):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO users VALUES(NULL,%s,%s,%s,now())"
        cursor.execute(sql,[
            email,
            password,
            nickname,
            ])
        user_id = cursor.lastrowid
        #写入默认角色 'user'
        sql_role = "INSERT INTO `role` (users_id, role) VALUES(%s, 'user')"
        cursor.execute(sql_role,[user_id])
        conn.commit() #提交事务
        return user_id  #返回插入数据id
    except Exception as e:
        print(e)
        conn.rollback()  #回滚事务
        return 0

if __name__ == "__main__":
    from pydantic import Field, BaseModel
    class RegistrationUsers(BaseModel):
        email: str = Field(..., description="邮箱号")
        nickname: str = Field(..., description="用户名")
        password: str = Field(..., description="密码")
    rs = RegistrationUsers(email="1607259232@qq.com",nickname="seanzhang",password="123456")
    save_registration_result(rs)
```

---

### 6. `password/service/PasswordService.py`（**整文件替换**，含修语法 bug）

```python
'''
    本模块是用户进行密码修改的功能实现，包括用户通过密码修改或者发送验证码来进行修改
'''
from password.dao.PasswordDao import query_users_by_email,change_password
from common.LoadRedisConn import LoadRedisConn
from login.utils.CreateCaptchaUtil import CreateCaptchaUtil
from common.JWTUtil import hash_password, verify_password
from email.mime.text import MIMEText
import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

#发送验证码修改密码
def send_captcha_for_password_change(email):
    results = query_users_by_email(email)
    if len(results) == 0:
        print("该邮箱未注册")
        return {
            "code":500,
            "msg":"邮箱未注册",
            "data":None
        }
    send_email=os.getenv("SEND_EMAIL")
    auth_code = os.getenv("AUTH_CODE")
    subject = "您正在通过邮箱进行影视问答系统的密码修改"
    create_captcha_util = CreateCaptchaUtil()
    captcha = create_captcha_util.captcha
    print(captcha)
    content =f"你本次修改密码的验证码为{captcha}，过期时间为5分钟"
    messages = MIMEText(content,"plain","utf-8")
    messages["From"] = send_email
    messages["To"] = email
    messages["Subject"] = subject
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp = smtplib.SMTP(smtp_server,smtp_port)
    smtp.starttls()
    smtp.login(send_email,auth_code)
    smtp.sendmail(send_email,email,messages.as_string())
    smtp.quit()
    try:
        redis_conn = LoadRedisConn.load_redis_conn()
        redis_conn.setex(email,300,captcha)
        LoadRedisConn.close_redis_conn(redis_conn)
        print("验证码已经发送！")
        return{
            "code":200,
            "msg":"验证码已发送",
            "data":{
                "nickname":results[0]["nickname"],
                "userId":results[0]["users_id"]
            }
        }
    except Exception as e:
        print(f"验证码发送失败！具体原因：{e}")
        return{
            "code":500,
            "msg":"验证码发送失败",
            "data":None
        }

def change_password_by_password(email, old_password, new_password):
    results = query_users_by_email(email)
    if len(results) > 0:
        #兼容旧明文密码：先校验 bcrypt 哈希，再兜底明文比较
        if verify_password(old_password, results[0]["password"]) or old_password == results[0]["password"]:
            print("密码正确，下面开始修改密码")
            change_password(email, hash_password(new_password))
            print("密码修改成功")
            return {
                "code":200,
                "msg":"密码修改成功",
                "data":None
            }
        else:
            print("密码不正确！")
            return {
                "code":500,
                "msg":"密码不正确",
                "data":None
            }
    else:
        print("您输入的邮箱未注册！")
        return {
            "code":500,
            "msg":"邮箱不存在",
            "data":None
        }

def change_password_by_captcha(email, captcha, new_password):
    redis_conn = LoadRedisConn().conn
    redis_captcha = redis_conn.get(email)
    if not redis_captcha:
        print("验证码过期！")
        return{
            "code":500,
            "msg":"验证码已过期",
            "data":None
        }
    if redis_captcha == captcha:
        print("验证通过，下面进行密码修改！")
        change_password(email, hash_password(new_password))
        print("密码修改成功!")
        return {
            "code":200,
            "msg":"修改密码成功",
            "data":None
        }
    else:
        print("验证码错误！")
        return {
            "code":500,
            "msg":"验证码不正确",
            "data":None
        }

if __name__ =="__main__":
    #change_password_by_password("123456@qq.com","654321","123456")
    #change_password_by_password("2012761893@qq.com", "123456", "654321")
    #send_captcha_for_password_change("2012761893@qq.com")
    change_password_by_captcha("2012761893@qq.com","939746","111111")
```

---

### 7. `admin/dao/AdminDao.py`（**整文件替换**）

```python
'''
    本模块是用来帮助管理员的数据库操作
'''
from common.LoadMySQLConn import LoadMySQLConn
from common.JWTUtil import hash_password

#根据用户名称查询用户信息
def query_users_by_nickname(name):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE nickname=%s"
    cursor.execute(sql,[name])
    results = cursor.fetchall()
    LoadMySQLConn.close_mysql_conn(cursor,conn)
    return results

#根据邮箱来查询用户信息
def query_users_by_email(email):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE email=%s"
    cursor.execute(sql,[email])
    results = cursor.fetchall()
    LoadMySQLConn.close_mysql_conn(cursor,conn)
    return results

#创建用户操作（默认密码 123456 哈希化 + 默认角色 'user'）
def create_users_with_email_nickname(email:str,nickname:str):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO users VALUES(NULL,%s,%s,%s,now())"
        cursor.execute(sql,[
            email,
            hash_password("123456"),
            nickname,
        ])
        user_id = cursor.lastrowid
        sql_role = "INSERT INTO `role` (users_id, role) VALUES(%s, 'user')"
        cursor.execute(sql_role,[user_id])
        conn.commit()
        return user_id  #返回创建用户的userid
    except Exception as e:
        print(e)
        conn.rollback()  #回滚事务
        return 0
    finally:
        LoadMySQLConn().close_mysql_conn(cursor,conn)

#根据用户名进行初始化密码操作，密码初始化为123456（哈希化）
def password_init_by_nickname(name):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    try:
        sql = "UPDATE users SET password=%s WHERE nickname=%s"
        cursor.execute(sql,[hash_password("123456"), name])
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        return 0
    finally:
        LoadMySQLConn.close_mysql_conn(cursor,conn)

#根据用户名删除一个用户信息
def delete_users_by_nickname(name:str):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM users WHERE nickname=%s"
        cursor.execute(sql,[name])
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(e)
        conn.rollback()
        return 0
    finally:
        LoadMySQLConn.close_mysql_conn(cursor,conn)
```

---

### 8. `chat/controller/ChatController.py`（**整文件替换**）

```python
'''
    对话的路由
'''

import json

from fastapi import APIRouter, Depends
from chat.service import ChatService
from starlette.responses import StreamingResponse
from common.JWTUtil import get_current_user

#整个聊天路由都要求登录；token 可走 Authorization 头或 ?token=（SSE 场景）
chat_router = APIRouter(dependencies=[Depends(get_current_user)])

#对话路由配置
@chat_router.get("/chat")
def chat(question:str, historyId:str):
    def chat_generator():
        for item in ChatService.chat(question,int(historyId)):  #控制流式输出
            yield f"data:{json.dumps({'content':str(item)})}\n\n"
        yield f"data:{json.dumps({'content':'[DONE]'})}\n\n"  #[DONE]表示结束
    return StreamingResponse(
        content = chat_generator(),
        media_type="text/event-stream"
    )
```

---

### 9. `history/controller/HistoryController.py`（**整文件替换**）

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

---

### 10. `admin/controller/AdminController.py`（**整文件替换**）

```python
'''
    管理员的路由
'''

from fastapi import APIRouter, Depends
from admin.service import AdminService
from admin.entity.AdminEntity import CreateUsersEntity, AdminEntity
from common.JWTUtil import token_check

#只有管理员角色能调用，普通用户 403
admin_router = APIRouter(dependencies=[Depends(token_check("admin"))])

#创建用户
@admin_router.post("/createUsers")
def create_users(create_users_entity:CreateUsersEntity):
    return AdminService.create_users(create_users_entity.email, create_users_entity.nickname)

#初始化用户密码
@admin_router.post("/initPassword")
def password_init_by_nickname(admin_entity:AdminEntity):
    return AdminService.password_init(admin_entity.nickname)

#删除用户
@admin_router.post("/deleteUsers")
def delete_users(admin_entity:AdminEntity):
    return AdminService.delete_users(admin_entity.nickname)
```

---

### 11. `password/controller/PasswordController.py`（**整文件替换**）

```python
'''
    本模块是用户实现密码修改的数据库操作的路由挂载
'''

from fastapi import APIRouter, Depends
from common.JWTUtil import get_current_user
from password.service import PasswordService
from password.entity.PasswordEntity import ChangePasswordCaptchaEntity,ChangePasswordPasswordEntity
password_router = APIRouter()

#修改密码发送验证码（公开）
@password_router.get("/sendCaptcha")
def send_captcha_for_password_change(email):
    return PasswordService.send_captcha_for_password_change(email)

#通过旧密码修改密码（需登录）
@password_router.post("/changePasswordPassword")
def change_password_by_password(change_password_password_entity:ChangePasswordPasswordEntity, current_user:dict=Depends(get_current_user)):
    return PasswordService.change_password_by_password(
        change_password_password_entity.email,
        change_password_password_entity.old_password,
        change_password_password_entity.new_password
        )

#通过验证码修改密码（忘记密码找回，保持公开）
@password_router.post("/changePasswordCaptcha")
def change_password_by_captcha(change_password_captcha_entity:ChangePasswordCaptchaEntity):
    return PasswordService.change_password_by_captcha(
        change_password_captcha_entity.email,
        change_password_captcha_entity.captcha,
        change_password_captcha_entity.new_password,
        )
```

---

## 三、前端完整代码（5 个文件）

> 路径相对 `my-vue-app/src/`。

### 12. `main.js`（**整文件替换**）

```js
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
//注册router
import router from "./router"
const app = createApp(App)
app.use(router)

//全局配置axios请求
import axios from "axios"  //导入axios包
axios.defaults.baseURL = "http://localhost:8000/" //服务器请求路径公共部分，即后端接口，将前端对接到后端
axios.defaults.headers.post['Content-Type'] = 'application/json' //post请求发送json数据给服务器
axios.defaults.headers.put['Content-Type'] = 'application/json'  //put请求发送json数据给服务器
app.config.globalProperties.$axios = axios //挂载axios，使用$axios替代原生axios

//请求拦截器：每次请求自动携带 token
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

//注册element-plus
import ElementPlus from 'element-plus'

// 注册md格式解析
// Markdown 配置
import { marked } from 'marked'
import DOMPurify from 'dompurify'

//  Markdown 配置
marked.setOptions({
  breaks: true,    // 支持换行
  gfm: true,       // GitHub 风格
  smartLists: true,
  smartypants: false
})

// Markdown 正则处理
function normalizeMarkdown(text) {
  return text
    .replace(/(#{1,6} )/g, '\n$1')
    .replace(/- /g, '\n- ')
}

// 全局 markdown 渲染方法
function renderMarkdown(text) {
  if (!text) return ''
  const rawHtml = marked.parse(normalizeMarkdown(text))
  return DOMPurify.sanitize(rawHtml)
}
app.config.globalProperties.$renderMarkdown = renderMarkdown

//导航守卫
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

app.mount('#app')
```

---

### 13. `router/index.js`（**整文件替换**）

```js
import {createRouter,createWebHistory} from "vue-router"

//创建路由对象
const router = createRouter({
    history:createWebHistory(),
    routes:[
        //登录页面路由配置
        {
            path:"/login",
            component:()=>import("../components/Login.vue")
        },
        //对话页面路由配置
        {
            path:"/chat",
            meta:{
                isLogin:true //需要拦截处理[登陆了才能访问，需要授权]
            },
            component:()=>import("../components/Chat.vue")
        },
        //用户注册页面路由配置
        {
            path:"/registration",
            meta:{
                isLogin: false
            },
            component:()=>import("../components/Registration.vue")
        },
        //用户修改密码路由配置
        {
            path:"/password",
            meta:{
                isLogin: true
            },
            component:()=>import("../components/Password.vue")
        },
        //管理员路由配置
        {
            path:"/admin",
            meta:{
                isLogin:true,
                requiresAdmin:true,   //新增：仅管理员可进
            },
            component:()=>import("../components/Admin.vue")
        },

    ]
})

export default router
```

---

### 14. `components/Login.vue`（**整文件替换**）

```vue
<template>
  <div>

    <!--登录卡片头部-->
    <div>
      <h2>用户登录</h2>
    </div>

      <!--Tab导航-->
      <div>
        <span @click="activeLoginMethod ='captcha'">通过验证码登录</span><br>
        <span @click="activeLoginMethod ='email_password'">通过邮箱密码登录</span><br>
        <span @click="activeLoginMethod ='nickname_password'">通过用户名密码登录</span><br>
      </div>

    <!--通过邮箱验证码登录-->
    <div v-show="activeLoginMethod==='captcha'">
      <form>
        邮箱号：<input type="text" :disabled="isSend" v-model="email"><br>
        验证码：<input type="text" :disabled="!isSend" v-model="captcha"><br>
        <button type="button" :disabled="isSend" @click="sendCaptcha">发送验证码</button>
        <button type="button" :disabled="!isSend" @click="loginByEmailCaptcha">登录</button>
      </form>
    </div>

  <!--通过邮箱密码登录-->
  <div v-show="activeLoginMethod==='email_password'">
      <form>
        邮箱号：<input type="text"  v-model="email"><br>
        密码：<input type="password"  v-model="password"><br>
        <button type="button" :disabled="(!email.trim()) ||(!password.trim())" @click="loginByEmailPassword">登录</button>
      </form>
    </div>

  <!--通过用户名密码登录-->
  <div v-show="activeLoginMethod==='nickname_password'">
      <form>
        用户名：<input type="text"  v-model="nickname"><br>
        密码：<input type="password"  v-model="password"><br>
        <button type="button" :disabled="(!nickname.trim()) ||(!password.trim())" @click="loginByNicknamePassword">登录</button>
      </form>
    </div>
  </div>

</template>

<script setup>
import {ref, getCurrentInstance, onMounted} from "vue";
import {useRouter} from "vue-router"
import {ElMessage} from 'element-plus'

let router = useRouter()
let proxy = getCurrentInstance().proxy

let email = ref("")
let captcha = ref("")
let nickname = ref("")
let password = ref("")

let isSend = ref(false)
let activeLoginMethod = ref("")

//定义发送验证码函数
function sendCaptcha(){
  isSend.value = !isSend.value
  proxy.$axios({
    url:"login/sendCaptcha",
    method:"get",
    params:{
      email:email.value
    }
  }).then(res=>{
    console.log(res)
    if(res.data.code===200) {
      alert("验证码已经发送！")
      ElMessage.success("验证码已发送，请查收")
      sessionStorage.setItem("nickname",res.data.data.nickname)
      sessionStorage.setItem("usersId",res.data.data.usersId)
    }
    else{
      ElMessage.error(res.data.msg)
    }
  })
}

//邮箱验证码登录函数
function loginByEmailCaptcha(){
  proxy.$axios({
    url:"login/loginByEmailCaptcha",
    method:"post",
    data:JSON.stringify({
      email:email.value,
      captcha:captcha.value,
    }),
  }).then(res=>{
    if(res.data.code ===200){
      alert("登录成功！")
      sessionStorage.setItem("access_token",res.data.data.access_token)
      sessionStorage.setItem("role",res.data.data.role)
      sessionStorage.setItem("nickname",res.data.data.nickname)
      sessionStorage.setItem("usersId",res.data.data.usersId)
      setTimeout(()=>{router.push("/chat")},1000)
    }
    else{
      alert(res.data.msg)
    }
  })
}

//邮箱密码登录函数
function loginByEmailPassword(){
  proxy.$axios({
    url:"login/loginByEmailPassword",
    method:"post",
    data:JSON.stringify({
      email:email.value,
      password:password.value,
    }),
  }).then(res=>{
    if(res.data.code ===200){
      alert("登录成功！")
      sessionStorage.setItem("access_token",res.data.data.access_token)
      sessionStorage.setItem("role",res.data.data.role)
      sessionStorage.setItem("nickname",res.data.data.nickname)
      sessionStorage.setItem("usersId",res.data.data.usersId)
      setTimeout(()=>{router.push("/chat")},1000)
    }
    else{
      alert(res.data.msg)
    }
  })
}

//用户名密码登录函数
function loginByNicknamePassword(){
  proxy.$axios({
    url:"login/loginByNicknamePassword",
    method:"post",
    data:JSON.stringify({
      nickname:nickname.value,
      password:password.value,
    }),
  }).then(res=>{
    if(res.data.code ===200){
      alert("登录成功！")
      sessionStorage.setItem("access_token",res.data.data.access_token)
      sessionStorage.setItem("role",res.data.data.role)
      sessionStorage.setItem("nickname",res.data.data.nickname)
      sessionStorage.setItem("usersId",res.data.data.usersId)
      setTimeout(()=>{router.push("/chat")},1000)
    }
    else{
      alert(res.data.msg)
    }
  })
}

</script>

<style scoped>

</style>
```

---

### 15. `components/Chat.vue`（**整文件替换**）

```vue
<template>
  <div>
    <!--左侧功能：展示历史记录以及新建一个对话-->
    <div>
      <div>RAG</div>
      <button @click="createNewChat">新对话</button>
    </div>

    <!--历史记录标题-->
    <div>
      <span>历史记录</span>
    </div>

    <!--一个完整窗口的全部上下文记录-->
    <div v-for="item in historyList" :key="item.historyId" @click="selectHistory(item.historyId)">
      <div>
        <div>{{item.question}}</div>
        <div>{{item.createTime}}</div>
      </div>
      <button @click.stop="deleteHistory(item.historyId)">删除</button>
    </div>

    <!--底部，当前用户的信息-->
    <div>
      <div>
        <span>{{nickname}}</span>
        <select @change = 'handleUserCommand($event.target.value)'>
          <option value="profile">个人中心</option>
          <option value="settings">设置</option>
          <option v-if="role==='admin'" value="admin">管理后台</option>
          <option value="logout">退出登录</option>
        </select>
      </div>
    </div>

    <!----------------------右侧,即对话主区域----------------------->
    <main>
      <header>
        <div>{{currentTitle}}</div>
        <div>{{nickname}}与基于影视的RAG问答助手</div>
      </header>

      <!--消息区-->
      <div ref ="messageBox">
        <div v-if="messages.length===0">
          <div>RAG</div>
          <div>你好,{{nickname}}</div>
          <div>我是基于影视的RAG问答助手，可以基于知识库为你解答问题</div>
          <div>
            <span v-for="q in suggestQuestions" :key="q" @click="quickAsk(q)">{{q}}</span>
          </div>
        </div>
        <!--一个窗口的全部对话记录-->
        <div v-for="(item,index) in messages" :key="index">
          <div>
            <div>{{item.role ==='assistant'?'基于影视的RAG问答助手':nickname}}</div>
            <div>
              <span v-if="item.role==='user'">{{item.content}}}</span>
              <div v-else v-html="$renderMarkdown(item.content)"></div>
            </div>
          </div>
        </div>
      </div>

      <!--底部输入区-->
      <div>
        <textarea
            v-model="question",
            rows="1"
            placeholder="向基于影视系统的RAG问答助手提问，enter发送，shift+enter换行"
            @keydown.enter.exact.prevent="handleEnter"
        ></textarea>
        <button :isdisabled="isButtonDisabled" @click="chat">
          <span v-show="!isLoading">发送</span>
          <span v-show="isLoading">加载中</span>
        </button>
      </div>

    </main>

  </div>
</template>

<script setup>
import {ref, watch,computed,getCurrentInstance, onMounted,nextTick} from "vue";
import {useRouter} from "vue-router"
import {ElMessage} from "element-plus"
//代理对象
let proxy = getCurrentInstance().proxy
//路由对象，用于登录跳转功能
let router = useRouter()

//控制发送按钮是否可以使用的布尔值
let isButtonDisabled = ref(true)
//用户输入的问题
let question = ref("")
//用户名
let nickname = ref("")
//当前用户角色，用于控制管理入口显隐
let role = ref("user")

//监听用户输入的问题
watch(question,(newQuestion)=>{
  console.log(newQuestion)
  if(newQuestion.length>0 && newQuestion.trim()){
    isButtonDisabled.value = false
  }
  else{
    isButtonDisabled.value = true
  }
})

//存储聊天记录的数组
let messages = ref([])
//控制loading按钮
let isLoading = ref(false)
//全局对话保存的history_id(默认为0)
let globalHistoryId = ref(0)

//空状态下的快捷提问建议
const suggestQuestions = [
    "推荐几部高分电影",
    "热门电影",
    "新上映的电影"
]

//左侧对话窗口记录
let historyList= ref([])

//聊天
function chat(){
  let myQuestion = question.value.trim()
  console.log(myQuestion)
  question.value = ""
  messages.value.push({role:"user",content:myQuestion})
  messages.value.push({role:"assistant",content:"ai努力回复中~~"})
  let params = new URLSearchParams({question:myQuestion,historyId:globalHistoryId.value})
  //SSE 无法带请求头，token 走 ?token=
  let sse = new EventSource("http://localhost:8000/chat/chat?"+params+"&token="+sessionStorage.getItem("access_token"))
  let s = ""
  sse.onmessage=(event)=>{
    let content = JSON.parse(event.data).content
    console.log(content)
    if (content === "[DONE]"){
      sse.close()
      console.log("SSE连接已经关闭")
      saveChatResult(myQuestion,s)
      isLoading.value = false
      return
    }
    s+= content
    messages.value[messages.value.length-1].content =s
  }
  sse.onerror = (event) => {
    console.log("SSE请求错误",event)
    isLoading.value = false
  }
  sse.onopen=()=>{
    console.log("建立SSE连接")
  }
}

//当前对话标题,动态显示聊天窗口顶部的标题
const currentTitle = computed(()=>{
  const cur = historyList.value.find(h=>h.id===globalHistoryId.value);
  return cur?cur.title:'新的对话';
})

//消息区DOM，自动滚动到底部
let messageBox = ref(null)

//监听消息变化，自动滚动到底部
watch(messages,()=>{
  nextTick(()=>{
    if(messageBox.value){
      messageBox.value.scrollTop = messageBox.value.scrollHeight
    }
  })
},{deep:true})

//点击左侧窗口记录进入一个完整的窗口
function selectHistory(historyId){
  globalHistoryId.value = historyId
  proxy.$axios({
    url:"history/queryHistoryList/"+historyId,
    method:"get"
  }).then(res=>{
    messages.value = res.data.data
  })
}

//保存对话结果
function saveChatResult(question,answer){
  let params = {
    userId:sessionStorage.getItem("usersId"),
    question:question,
    answer:answer,
    parentId:globalHistoryId.value,
  }
  proxy.$axios({
    url:"history/saveChatResult",
    method:"post",
    data:JSON.stringify(params)
  }).then(res=>{
    if(globalHistoryId.value === 0) {
      globalHistoryId.value = res.data.data
      queryHistoryMenu()
      }
  })
}

//加载历史对话菜单，即左侧窗口记录
function queryHistoryMenu(){
  proxy.$axios({
    url:"history/queryHistoryMenu/"+sessionStorage.getItem("usersId"),
    method:"get",
  }).then(res=>{
    historyList.value=res.data.data
  })
}

//键盘enter键进行消息的发送
function handleEnter(){
  if(!isButtonDisabled.value) {
    chat()
  }
}

//新建对话
function createNewChat(){
  globalHistoryId.value = 0
  messages.value=[]
}

//加载页面后执行，加载页面后挂载历史记录菜单
onMounted(()=>{
  nickname.value = sessionStorage.getItem("nickname")||"undefined"
  role.value = sessionStorage.getItem("role") || "user"
  queryHistoryMenu()
})

//用户菜单命令处理
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

//快速提问
function quickAsk(text){
  question.value=text
  chat()
}
</script>

<style scoped>

</style>
```

---

### 16. `components/Password.vue`（**整文件替换**）

```vue
<template>
 <div>
   <div>
     <h2>用户修改密码</h2>
   </div>

   <div>
     <span @click="activePasswordMethod='captcha'">通过邮箱验证码修改</span><br>
     <span @click="activePasswordMethod='password'">通过旧密码修改</span>
   </div>

   <!--通过邮箱验证码修改-->
   <div v-show="activePasswordMethod==='captcha'">
     <form>
       邮箱号：<input type="text" :disabled="isSend" v-model="email"><br>
       验证码：<input type="text" :disabled="!isSend" v-model="captcha"><br>
       新密码：<input type="password" :disabled="!isSend" v-model="new_password"><br>
       <button type="button" :disabled="isSend" @click="sendCaptcha">发送验证码</button>
       <button type="button" :disabled="(!isSend)||(!email.trim())||(!captcha.trim())||(!new_password.trim())" @click="changePasswordCaptcha">修改密码</button>
     </form>
   </div>

   <!--通过邮箱旧密码修改-->
   <div v-show="activePasswordMethod==='password'">
     <form>
       邮箱号：<input type="text"  v-model="email"><br>
       旧密码：<input type="password"  v-model="old_password"><br>
       新密码：<input type="password"  v-model="new_password"><br>
       <button type="button" :disabled="(!email.trim())||(!old_password.trim())||(!new_password.trim())" @click="changePasswordPassword">修改密码</button>
     </form>
   </div>
 </div>

</template>

<script setup>
import {ref, getCurrentInstance, onMounted} from "vue";
import {useRouter} from "vue-router"

let proxy = getCurrentInstance().proxy
let router = useRouter()

let activePasswordMethod = ref("")
let isSend = ref(false)

let email=ref("")
let old_password=ref("")
let new_password=ref("")
let captcha = ref("")

//定义发送验证码函数
function sendCaptcha(){
  isSend.value = !isSend.value
  proxy.$axios({
    url:"password/sendCaptcha",
    method:"get",
    params:{
      email:email.value
    }
  }).then(res=>{
    if(res.data.code===200){
      alert("验证码已经发送，请查收")
      sessionStorage.setItem("nickname",res.data.data.nickname)
      sessionStorage.setItem("usersId",res.data.data.usersId)
    }
    else {
      alert(res.data.msg)
    }
  })
}

//通过旧密码修改新密码（改密成功后需要重新登录，清空会话）
function changePasswordPassword(){
  proxy.$axios({
    url:"password/changePasswordPassword",
    method:"post",
    data:JSON.stringify({
      email:email.value,
      old_password:old_password.value,
      new_password:new_password.value
    })
  }).then(res=>{
    if(res.data.code===200){
      alert("密码修改成功！下面跳转到登录页面！请重新登录")
      sessionStorage.clear()
      email.value=""
      old_password.value=""
      new_password.value=""
      setTimeout(()=>{router.push("/login")},1000)
    }
    else {
      alert(res.data.msg)
    }
  })
}

//通过验证码修改密码（忘记密码找回，公开流程）
function changePasswordCaptcha() {
  proxy.$axios({
    url: "password/changePasswordCaptcha",
    method: "post",
    data: JSON.stringify({
      email: email.value,
      captcha: captcha.value,
      new_password: new_password.value
    })
  }).then(res => {
    if(res.data.code===200){
      alert("密码修改成功！下面跳转到登录页面！请重新登录")
      sessionStorage.clear()
      email.value = ""
      captcha.value = ""
      new_password.value = ""
      setTimeout(()=>{router.push("/login")},1000)
    }
    else {
      alert(res.data.msg)
    }
  })
}
</script>

<style scoped>

</style>
```

---

## 四、无需改动的文件

- `my-vue-app/src/components/Admin.vue` —— token 由 axios 拦截器自动携带，权限由后端 `token_check("admin")` 403 兜底 + 前端路由守卫拦截，无需改动。
- `my-vue-app/src/components/Registration.vue` —— 注册流程本身公开，无需改动。
- 各模块的 `entity/*.py`、`history`/`chat` 的 `service`、`dao`（登录/历史/密码/注册的 DAO 已在上面列出）等，均无需改动。

---

## 五、改完自测（验证步骤）

1. 先执行「数据库」那一步的 SQL，`SELECT * FROM \`role\`;` 确认表结构。
2. 后端 `uvicorn main:app`（端口 8000）、前端 `npm run dev`（端口 8080）。
3. 新注册一个用户 → MySQL `users.password` 应为 `$2b$...` 开头的哈希，`role` 表多一条 `'user'`。
4. 老明文用户登录一次 → 登录成功，且该行密码被自动升级成哈希（懒迁移生效）。
5. 未登录直访 `/chat` → 前端重定向 `/login`；未带 token `curl` 调 `history/queryHistoryMenu/1` → 401。
6. 登录后正常聊天 → 流式输出正常（token 走 `?token=`）。
7. A 账号登录，请求 `history/queryHistoryMenu/{别人的id}` → 仍只返回 A 自己的历史（IDOR 已封）。
8. 普通用户（role='user'）登录后调 `admin/deleteUsers` → 403；前端访问 `/admin` 被守卫拦回 `/chat`。
9. 管理员（role='admin'）登录后调 `admin/deleteUsers` → 200，且聊天页菜单出现「管理后台」。
10. 回归：未登录也能走「验证码找回/改密」（`password/sendCaptcha` + `password/changePasswordCaptcha` 仍公开）。

---

## 六、配置建议（可选，按需改 `.env`）

- `ACCESS_TOKEN_EXPIRE_MINUTES=10` 建议改成 `1440`（1 天），否则 10 分钟就掉线要重新登录。
- `SECRET_KEY` 建议换成随机长串（如 `openssl rand -hex 32` 的结果）。

> 说明/边界（本期未做）：refresh token、Redis 黑名单登出踢人、HTTPS 强制；`queryHistoryList/{historyId}` 仍按 historyId 定位（未做「该记录是否属于当前用户」的所有权校验，属暂缓项）。

---

## 七、改动点标注（行内注释标记）

> 图例：
> - 后端 Python：`# ⬅ 新增` / `# ⬅ 修改`
> - 前端 JS：`// ⬅ 新增` / `// ⬅ 修改`
> - Vue 模板：`<!-- ⬅ 新增 -->` / `<!-- ⬅ 修改 -->`
>
> 下面每个文件**只列改动涉及的行段**；没列出来的部分与原代码完全一致（完整版见上面二、三节）。

---

### 后端

#### 1. `common/JWTUtil.py` —— 整文件重写

**改动摘要**：原文件从未被业务调用，且有多处 bug。本次整体重写并真正接入。修掉的 bug：`HTTPException` 来源（原来误从 aiohttp 引入）、`ALGORITHM` 环境变量大小写（原来读 `algorithm` → `None`）、`timedelta(minutes=字符串)`、`verify_token` 用 `return` 而非 `raise`、`token_check` 重复校验且用 `roleName`、空 `tokenUrl`。关键改动：

```python
from fastapi import Depends, Header, HTTPException, Query   # ⬅ 修改：原来 import aiohttp 的 HTTPException

SECRET_KEY = os.getenv("SECRET_KEY")                         # ⬅ 修改：原来每次现读
ALGORITHM = os.getenv("ALGORITHM", "HS256")                  # ⬅ 修改：原来读小写 "algorithm"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # ⬅ 修改：原来没 int()，str 直接传 timedelta 会报错

def hash_password(plain: str) -> str:                        # ⬅ 修改：改用 bcrypt 直用（去掉 passlib）
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="登录凭证无效或已过期")  # ⬅ 修改：原来是 return，等于不抛异常

def get_current_user(
    authorization: str = Header(default=None),   # ⬅ 新增：同时支持 Authorization 头和 ?token= 两种取 token
    token: str = Query(default=None),            # ⬅ 新增：SSE 场景走查询参数
) -> dict:
    ...
    return {
        "user_id": int(payload.get("sub")),      # ⬅ 新增：统一返回 user_id / nickname / role
        "nickname": payload.get("nickname"),
        "role": payload.get("role", "user"),
    }

def token_check(required_role: str):            # ⬅ 修改：原来 *roles + roleName 混搭，简化为单角色 admin 校验
    def check_role(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") != required_role:
            raise HTTPException(status_code=403, detail="无权限执行该操作")  # ⬅ 修改：无权限返回 403
        return current_user
    return check_role
```

---

#### 2. `login/dao/LoginDao.py` —— 仅新增 2 个函数

**改动摘要**：原先只有 `query_users_by_email`、`query_users_by_nickname`，保持不变；新增下面两个函数。

```python
#根据用户id查询其角色（role 表；无记录由调用方按 'user' 兜底）
def query_role_by_user_id(users_id):              # ⬅ 新增
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    sql = "SELECT role FROM `role` WHERE users_id=%s"
    cursor.execute(sql,[users_id])
    results = cursor.fetchall()
    LoadMySQLConn.close_mysql_conn(cursor,conn)
    return results

#根据邮箱更新密码（用于存量明文密码的“懒迁移”）
def update_password_by_email(email, hashed_password):   # ⬅ 新增
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

#### 3. `login/service/LoginService.py` —— 5 处改动

**改动摘要**：加导入、加两个助手函数、三个登录方法都改为「校验密码 + 取角色 + 签发 token」。`send_captcha` 不变。

```python
from common.JWTUtil import hash_password, verify_password, create_token   # ⬅ 新增

#密码校验 + 懒迁移：存量密码是明文，登录成功后自动升级为 bcrypt 哈希
def _verify_and_upgrade(plain_password, stored_password, email):   # ⬅ 新增
    if stored_password.startswith(("$2a$", "$2b$", "$2y$")):
        return verify_password(plain_password, stored_password)
    if plain_password == stored_password:
        LoginDao.update_password_by_email(email, hash_password(plain_password))  # ⬅ 新增：明文比对成功就升级
        return True
    return False

#查询用户角色；role 表里无记录时默认普通用户
def _get_role(users_id):        # ⬅ 新增
    rows = LoginDao.query_role_by_user_id(users_id)
    return rows[0]["role"] if rows else "user"

#通过邮箱和验证码登录
def login_by_email_captcha(email, captcha):
    redis_conn = LoadRedisConn().conn
    redis_captcha = redis_conn.get(email)
    if not redis_captcha:
        return {"code":500,"msg":"验证码已过期","data":None}
    if redis_captcha == captcha:
        results = LoginDao.query_users_by_email(email)                  # ⬅ 新增：原来这里直接 data:None
        if len(results) == 0:
            return {"code":500, "msg":"邮箱未注册", "data":None}
        role = _get_role(results[0]["users_id"])                        # ⬅ 新增
        token = create_token({"sub": str(results[0]["users_id"]), "nickname": results[0]["nickname"], "role": role})  # ⬅ 新增
        return {"code":200,"msg":"登录成功","data":{
            "access_token": token,                                       # ⬅ 新增
            "nickname": results[0]["nickname"],
            "usersId": results[0]["users_id"],
            "role": role                                                # ⬅ 新增
        }}
    return {"code":500,"msg":"验证码错误","data":None}

#通过邮箱和保存的密码登录
def login_by_email_password(email:str, password:str):
    results = LoginDao.query_users_by_email(email)
    if len(results) == 0:
        return {"code":500,"msg":"邮箱未注册","data":None}
    if _verify_and_upgrade(password, results[0]["password"], email):   # ⬅ 修改：原来 password == results[0]["password"]
        role = _get_role(results[0]["users_id"])                        # ⬅ 新增
        token = create_token({"sub": str(results[0]["users_id"]), "nickname": results[0]["nickname"], "role": role})  # ⬅ 新增
        return {"code":200,"msg":"登录成功","data":{
            "access_token": token,                                       # ⬅ 新增
            "nickname": results[0]["nickname"], "usersId": results[0]["users_id"], "role": role  # ⬅ 新增
        }}
    return {"code":500,"msg":"密码错误","data":None}

#通过用户名和保存的密码登录
def login_by_nickname_password(nickname:str, password:str):
    results = LoginDao.query_users_by_nickname(nickname)
    if len(results) == 0:
        return {"code": 500, "msg": "用户名未注册", "data": None}
    if _verify_and_upgrade(password, results[0]["password"], results[0]["email"]):  # ⬅ 修改
        role = _get_role(results[0]["users_id"])                        # ⬅ 新增
        token = create_token({"sub": str(results[0]["users_id"]), "nickname": results[0]["nickname"], "role": role})  # ⬅ 新增
        return {"code": 200, "msg": "登录成功", "data": {
            "access_token": token, "nickname": results[0]["nickname"], "usersId": results[0]["users_id"], "role": role  # ⬅ 新增
        }}
    return {"code": 500, "msg": "密码错误", "data": None}
```

---

#### 4. `registration/service/RegistrationService.py` —— 2 处改动

**改动摘要**：加导入 + 入库前哈希密码。

```python
from common.JWTUtil import hash_password                 # ⬅ 新增

                save_registration_result(email, hash_password(password), nickname)  # ⬅ 修改：原来直接存明文 password
```

---

#### 5. `registration/dao/RegistrationDao.py` —— 1 处改动

**改动摘要**：用户入库后，用 `lastrowid` 拿到新 id，再写入默认角色 `'user'`（同一事务）。

```python
        user_id = cursor.lastrowid                      # ⬅ 新增
        sql_role = "INSERT INTO `role` (users_id, role) VALUES(%s, 'user')"  # ⬅ 新增
        cursor.execute(sql_role,[user_id])              # ⬅ 新增
        conn.commit()
        return user_id                                  # ⬅ 修改：原来直接 return cursor.lastrowid
```

---

#### 6. `password/service/PasswordService.py` —— 4 处改动

**改动摘要**：加导入；校验/写入改用哈希（兼容旧明文）；顺带修 `change_password_by_captcha` 返回字典缺逗号的语法 bug。

```python
from common.JWTUtil import hash_password, verify_password   # ⬅ 新增

def change_password_by_password(email, old_password, new_password):
    ...
        if verify_password(old_password, results[0]["password"]) or old_password == results[0]["password"]:  # ⬅ 修改：原来 old_password == results[0]["password"]
            change_password(email, hash_password(new_password))   # ⬅ 修改：原来直接存明文 new_password

def change_password_by_captcha(email, captcha, new_password):
    ...
        change_password(email, hash_password(new_password))   # ⬅ 修改：原来直接存明文
        return {
            "code":200,
            "msg":"修改密码成功",     # ⬅ 修改：原行末少了逗号（顺带修复）
            "data":None               # ⬅ 修改：原来误写成 "data:None"（语法错误，顺带修复）
        }
```

---

#### 7. `admin/dao/AdminDao.py` —— 3 处改动

**改动摘要**：加导入；建号默认密码哈希 + 写默认角色；重置密码哈希。

```python
from common.JWTUtil import hash_password                 # ⬅ 新增

        sql = "INSERT INTO users VALUES(NULL,%s,%s,%s,now())"
        cursor.execute(sql,[email, hash_password("123456"), nickname])  # ⬅ 修改：原来直接 "123456"
        user_id = cursor.lastrowid                        # ⬅ 新增
        sql_role = "INSERT INTO `role` (users_id, role) VALUES(%s, 'user')"  # ⬅ 新增
        cursor.execute(sql_role,[user_id])                # ⬅ 新增
        conn.commit()

        sql = "UPDATE users SET password=%s WHERE nickname=%s"          # ⬅ 修改：原来 password='123456' 写死
        cursor.execute(sql,[hash_password("123456"), name])             # ⬅ 修改
```

---

#### 8. `chat/controller/ChatController.py` —— 2 处改动

```python
from fastapi import APIRouter, Depends                     # ⬅ 修改：原来只 import APIRouter
from common.JWTUtil import get_current_user               # ⬅ 新增

chat_router = APIRouter(dependencies=[Depends(get_current_user)])  # ⬅ 修改：原来 chat_router = APIRouter()
```

> `chat(question, historyId)` 签名不变；`get_current_user` 里声明了 `token: str = Query(...)`，前端 `?token=` 自动识别。

---

#### 9. `history/controller/HistoryController.py` —— 整文件替换（加鉴权 + 修 IDOR）

```python
from fastapi import APIRouter, Depends                     # ⬅ 修改
from common.JWTUtil import get_current_user               # ⬅ 新增

history_router = APIRouter(dependencies=[Depends(get_current_user)])  # ⬅ 修改：整个路由要求登录

@history_router.get("/queryHistoryMenu/{usersId}")
def query_history_menu(usersId:int, current_user:dict=Depends(get_current_user)):  # ⬅ 修改：加 current_user
    return HistoryService.query_history_menu(current_user["user_id"])   # ⬅ 修改：忽略 URL 里的 usersId，改用登录用户 id（修 IDOR）

@history_router.post("/saveChatResult")
def save_chat_result(save_chat_results_entity:SaveChatResultsEntity, current_user:dict=Depends(get_current_user)):  # ⬅ 修改
    return HistoryService.save_chat_result(
        current_user["user_id"],                           # ⬅ 修改：原来用 body 里的 userId，改用登录用户 id
        ...
        )
```

---

#### 10. `admin/controller/AdminController.py` —— 2 处改动

```python
from fastapi import APIRouter, Depends                     # ⬅ 修改
from common.JWTUtil import token_check                    # ⬅ 新增

admin_router = APIRouter(dependencies=[Depends(token_check("admin"))])  # ⬅ 修改：只有 admin 角色能调，普通用户 403
```

---

#### 11. `password/controller/PasswordController.py` —— 2 处改动

```python
from fastapi import APIRouter, Depends                     # ⬅ 修改
from common.JWTUtil import get_current_user               # ⬅ 新增

#通过旧密码修改密码（需登录）
@password_router.post("/changePasswordPassword")
def change_password_by_password(change_password_password_entity:ChangePasswordPasswordEntity, current_user:dict=Depends(get_current_user)):  # ⬅ 修改：加 current_user
    ...
```

> `sendCaptcha`、`changePasswordCaptcha` 保持公开，未加依赖（否则忘记密码的人无法改密）。

---

### 前端（`my-vue-app/src/`）

#### 12. `main.js` —— 2 处改动

```js
//请求拦截器：每次请求自动携带 token
axios.interceptors.request.use(config => {                 // ⬅ 新增：整块
  const token = sessionStorage.getItem("access_token")
  if (token) {
    config.headers["Authorization"] = "Bearer " + token
  }
  return config
})

//响应拦截器：401 时清空会话并跳回登录页
axios.interceptors.response.use(                           // ⬅ 新增：整块
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      sessionStorage.clear()
      router.push("/login")
    }
    return Promise.reject(error)
  }
)

//导航守卫
router.beforeEach((to,from,next)=>{                        // ⬅ 修改：整块重写
  if(to.meta.isLogin){
    const token = sessionStorage.getItem("access_token")   // ⬅ 修改：原来判 nickname
    if(token===null || token.length===0){
      next("/login")
      return
    }
    if(to.meta.requiresAdmin){                            // ⬅ 新增：管理员页额外判角色
      if(sessionStorage.getItem("role")==="admin"){
        next()
      }else{
        next("/chat")
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

#### 13. `router/index.js` —— 1 处改动

```js
        {
            path:"/admin",
            meta:{
                isLogin:true,
                requiresAdmin:true,   // ⬅ 新增：仅管理员可进
            },
            component:()=>import("../components/Admin.vue")
        },
```

---

#### 14. `components/Login.vue` —— 3 处改动（3 个登录成功回调都加存取 token）

```js
    if(res.data.code ===200){
      alert("登录成功！")
      sessionStorage.setItem("access_token",res.data.data.access_token)   // ⬅ 新增
      sessionStorage.setItem("role",res.data.data.role)                   // ⬅ 新增
      sessionStorage.setItem("nickname",res.data.data.nickname)           // ⬅ 新增（验证码登录原来漏存）
      sessionStorage.setItem("usersId",res.data.data.usersId)             // ⬅ 新增（验证码登录原来漏存）
      setTimeout(()=>{router.push("/chat")},1000)
    }
```

> 上面这段在 `loginByEmailCaptcha`、`loginByEmailPassword`、`loginByNicknamePassword` 三个函数里各加一次；邮箱密码/用户名密码两个原本已存 nickname、usersId，这次补存 `access_token`、`role`。

---

#### 15. `components/Chat.vue` —— 6 处改动

**模板**：用户菜单加「管理后台」选项（仅 admin 可见）。

```html
        <select @change = 'handleUserCommand($event.target.value)'>
          <option value="profile">个人中心</option>
          <option value="settings">设置</option>
          <option v-if="role==='admin'" value="admin">管理后台</option>   <!-- ⬅ 新增 -->
          <option value="logout">退出登录</option>
        </select>
```

**脚本**：

```js
import {ref, watch,computed,getCurrentInstance, onMounted,nextTick} from "vue";
import {useRouter} from "vue-router"        // ⬅ 新增
import {ElMessage} from "element-plus"      // ⬅ 新增：原来用到 ElMessage 却没 import（修既有报错）

let proxy = getCurrentInstance().proxy
let router = useRouter()                    // ⬅ 新增：原来没定义 router，logout 无法跳转
let role = ref("user")                      // ⬅ 新增

//聊天
function chat(){
  ...
  let sse = new EventSource("http://localhost:8000/chat/chat?"+params+"&token="+sessionStorage.getItem("access_token"))  // ⬅ 修改：SSE 无法带请求头，token 走 ?token=
  ...
}

onMounted(()=>{
  nickname.value = sessionStorage.getItem("nickname")||"undefined"
  role.value = sessionStorage.getItem("role") || "user"    // ⬅ 新增
  queryHistoryMenu()
})

function handleUserCommand(command){
  switch(command){
    case "profile": ...
    case "settings": ...
    case "admin":                        // ⬅ 新增
      router.push("/admin")              // ⬅ 新增
      break
    case "logout":
      logout()
      break
  }
}

//退出登录：清空会话并回登录页
function logout(){                       // ⬅ 新增：原来只被调用、没定义
  sessionStorage.clear()
  router.push("/login")
}
```

---

#### 16. `components/Password.vue` —— 1 处改动（2 个成功回调都加清会话）

```js
    if(res.data.code===200){
      alert("密码修改成功！下面跳转到登录页面！请重新登录")
      sessionStorage.clear()             // ⬅ 新增：改密后清掉旧 token，强制重新登录
      email.value=""
      old_password.value=""
      new_password.value=""
      setTimeout(()=>{router.push("/login")},1000)
    }
```

> `changePasswordPassword` 与 `changePasswordCaptcha` 两个成功分支都加了 `sessionStorage.clear()`。

---

## 八、改动点速查表

| # | 文件 | 改动类型 | 一句话说明 |
|---|---|---|---|
| 1 | `common/JWTUtil.py` | 整文件重写 | 修 bug + 签发/校验/取当前用户/角色鉴权 |
| 2 | `login/dao/LoginDao.py` | 新增 2 函数 | 查角色、按邮箱改密码（懒迁移） |
| 3 | `login/service/LoginService.py` | 5 处 | 哈希校验 + 取角色 + 签发 token |
| 4 | `registration/service/RegistrationService.py` | 2 处 | 注册时哈希密码 |
| 5 | `registration/dao/RegistrationDao.py` | 1 处 | 注册时写默认角色 'user' |
| 6 | `password/service/PasswordService.py` | 4 处 | 改密哈希化 + 修语法 bug |
| 7 | `admin/dao/AdminDao.py` | 3 处 | 建号/重置密码哈希 + 写默认角色 |
| 8 | `chat/controller/ChatController.py` | 2 处 | 聊天接口加登录鉴权 |
| 9 | `history/controller/HistoryController.py` | 整文件替换 | 加鉴权 + 修 IDOR |
| 10 | `admin/controller/AdminController.py` | 2 处 | admin 接口只用 admin 角色 |
| 11 | `password/controller/PasswordController.py` | 2 处 | 仅「凭旧密码改密」加鉴权 |
| 12 | `main.js` | 2 处 | axios 拦截器 + 守卫判 token/角色 |
| 13 | `router/index.js` | 1 处 | /admin 加 requiresAdmin |
| 14 | `Login.vue` | 3 处 | 登录成功存 token/role |
| 15 | `Chat.vue` | 6 处 | SSE 带 token、logout、按角色显隐菜单 |
| 16 | `Password.vue` | 1 处 | 改密成功后清会话 |