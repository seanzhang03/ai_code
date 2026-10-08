#用于接收登录的数据的类

from pydantic import Field,BaseModel

class LoginUsers(BaseModel):
    #邮箱号
    email:str = Field(...,description="邮箱号") #...占位符，标识该字段必填
    #验证码
    captcha:str =Field(...,description="验证码")