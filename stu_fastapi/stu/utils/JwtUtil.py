from datetime import datetime,timedelta,timezone
from typing import Optional

from fastapi import HTTPException
from jose import JWTError,jwt
import os
from dotenv import load_dotenv

load_dotenv(

)

#创建令牌
def create_token(
        data:dict,
        expires_data:Optional[timedelta]=None
)->str:
    #param data：需要存入载荷的数据内容
    #return：生成的token字符串
    #拷贝数据内容
    to_encode = data.copy()
    #计算token多久过期 = 当前时间+过期时间
    expires_time=datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    #把过期时间存入载荷
    to_encode.update({"exp":expires_time,"iat":datetime.now(timezone.utc)})
    #创建令牌
    return jwt.encode(
        to_encode,
        os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM")
    )

#验证令牌
def verify_token(token:str) ->dict:
    #param token:要验证的token字符串
    #return：验证通过的载荷数据
    try:
        payload = jwt.decode(
            token,os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")]
        )
        return payload
    except JWTError:
        #抛出没有token异常
        raise HTTPException(status_code=401,detail="Invalid token")

#导入fastapi继承的oth2
#能够解析客户端传来的Authorization内容，自动在Authorization提取token字段
from fastapi.security import OAuth2PasswordBearer
#tokenURL = 生成token的接口地址
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/stu/login")
from fastapi import Depends,Header

#获取当前用户数据内容
def get_current_user(
        token:str=Depends(oauth2_schema),
):
    user_dict = verify_token(token)
    return user_dict

#token认证
def token_check(*roles:str):
    print(roles)
    def role_check(token:str=Depends(oauth2_schema)):
        user_dict = verify_token(token)
        user_dict = {"roleName":"admin"}
        roleName = user_dict.get("roleName")
        print(roleName)
        #判断一个字符串是否包含另一个子字符串
        if roleName in roles: #?roles白名单
            return user_dict
        else:
            raise HTTPException(
                status_code=401,
                detail="权限不足"
            )
    return role_check













