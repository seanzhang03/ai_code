'''
    定义一个包含登录信息的类的实体，所有的post请求都不能够直接传值，要用实体代替
'''
from pydantic import Field,BaseModel

#验证码登录实体
class LoginCaptchaEntity(BaseModel):
    #邮箱号
    email:str = Field(...,description="邮箱号")
    #验证码
    captcha:str = Field(...,description="验证码")

#邮箱密码登录实体
class LoginEmailPasswordEntity(BaseModel):
    #邮箱号
    email:str = Field(...,description="邮箱号")
    #密码
    password:str = Field(...,description="密码")

class LoginNicknamePasswordEntity(BaseModel):
    #用户名
    nickname:str = Field(...,description="用户名")
    #密码
    password:str = Field(...,description="密码")