#1.创建令牌
#2.验证令牌
from datetime import datetime,timedelta,timezone
from typing import Optional

from aiohttp.web_exceptions import HTTPException
import jwt
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
        return HTTPException(status_code=401,detail="Invalid token")


    #print(verify_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInJvbGVOYW1lIjoidXNlciIsImV4cCI6MTc4OTkzODk1OCwiaWF0IjoxNzg5OTM4MzU4fQ.eEJHWL898LVJXXyLdSKMNQpzHtTP0kvPaoXmTwLmfAo"))