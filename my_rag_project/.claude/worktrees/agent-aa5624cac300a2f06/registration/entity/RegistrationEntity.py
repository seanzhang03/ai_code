'''
    定义接收注册数据的类
'''
from pydantic import Field,BaseModel

class RegistrationEntity(BaseModel):
    #邮箱号
    email:str = Field(...,description="邮箱号")
    #用户名
    nickname:str = Field(...,description="用户名")
    #密码
    password:str = Field(...,description="密码")