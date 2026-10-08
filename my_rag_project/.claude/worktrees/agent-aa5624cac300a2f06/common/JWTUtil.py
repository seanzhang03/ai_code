'''
    JWT相关工具
'''
from jose import JWTError,jwt
from dotenv import load_dotenv
import os
from fastapi import Depends,Header,HTTPException
from typing import Optional
from datetime import datetime,timedelta,timezone
load_dotenv()

from passlib.context import CryptContext
#jwt对象：Header+Payload+Signature

#加密对象---加密算法bcry
crypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#密码加密函数
def hash_password(password)->str:
    return crypt_context.hash(password)

#密码验证函数
def verify_password(plain_password:str,hashed_password:str)->bool:
    return crypt_context.verify(plain_password,hashed_password)  #返回一个bool值

#根据用户id和昵称创建jwt令牌
def create_token(data:dict,expires_data:Optional[timedelta]=None)->str:
    #参数 data：需要存入载荷(payload)的数据内容,拷贝数据内容
    to_encode = data.copy()
    #计算token多久过期 timedeleta构造时间差对象
    expires_time=datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    #将过期时间存入载荷 exp：过期时间 iat：签发时间
    to_encode.update({"exp":expires_time,"iat":datetime.now(timezone.utc)})
    #创建令牌,返回一个token对象
    return jwt.encode(
        to_encode,  #要编码的对象
        os.getenv("SECRET_KEY"),        #密钥
        algorithm=os.getenv("ALGORITHM") #算法名
    )

#验证令牌，最后传出令牌中载荷的数据(字典)
def verify_token(token:str)->dict:
    #参数 token：要验证的token字符串
    try:
        payload =jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")]
        )
        #返回载荷，其结果是create_token时传入的data：dict字典
        return payload
    except JWTError:
        #抛出没有token的异常
        raise HTTPException(status_code=401,detail="Invalid token")

#导入fastapi继承的oth2
#能够解析客户端传来的Authorization内容，自动在Authorization提取token字段
#告诉 FastAPI"从请求头 Authorization: Bearer <token> 里取 token
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login/loginByEmailCaptcha")

#主函数(参数=Depends(get_current_user))
#暂停执行主函数。
#分析依赖：它去查看 get_current_user 这个函数需要什么参数。它发现 get_current_user 需要一个参数：token: str = Depends(oauth2_schema)。
#解决嵌套依赖：FastAPI 发现 get_current_user 的参数 token 也是一个依赖（Depends(oauth2_schema)）。于是它转头去执行 oauth2_schema。
#提取数据：oauth2_schema（也就是 OAuth2PasswordBearer）会自动去当前请求的 HTTP Headers 里面找 Authorization 字段，提取出真实的 Token 字符串。
#自动传参（注入）：FastAPI 拿到了这个真实的 Token 字符串后，自动把它传给了 get_current_user 函数，相当于它在背后执行了 get_current_user(token="提取到的真实Token")。
#获取结果：get_current_user 执行完毕，返回了 user_dict。
#继续执行主函数：FastAPI 把拿到的 user_dict 赋值给 me 函数的 user_info 参数，然后终于开始执行 me 函数内部的代码。
#得到当前的用户的数据内容
def get_current_user(
        token:str=Depends(oauth2_schema)  #必须是传参Authorization=Bearer Token,若没传，则直接抛出401
):
    user_info_dict = verify_token(token)
    return user_info_dict

#token认证
def token_check(*roles:str):  #roles:可变位置参数
    print(roles)
    def role_check(token:str=Depends(oauth2_schema)):
        #判断一个字符串是否包含另一个子字符串
        user_dict = verify_token(token)
        role = user_dict.get("role")
        # 判断一个字符串是否包含另一个子字符串
        if role in roles:  #roles是管理员名单
            return user_dict
        else:
            raise HTTPException(
                status_code=401,
                detail="权限不足"
            )
    return role_check

if __name__ == "__main__":
    #print(create_token({"users_id":"1","niciname":"cc","roleName":"admin"}))
    #print(verify_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2Vyc19pZCI6IjEiLCJuaWNpbmFtZSI6ImNjIiwicm9sZU5hbWUiOiJhZG1pbiIsImV4cCI6MTc4OTk2NjQxNywiaWF0IjoxNzg5OTY1ODE3fQ.OAlvJgcHIaP3YtrLov4cT_Ow7z4nb0MreyScMj-5gSA"))
    def a(token:str=Depends(oauth2_schema)):
        print(token)
    a()