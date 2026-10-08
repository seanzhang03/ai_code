from pydantic import Field,BaseModel

class CreateUsersEntity(BaseModel):
    #邮箱
    email:str = Field(...,description="邮箱号")
    #用户名
    nickname:str = Field(...,description="用户名")

class AdminEntity(BaseModel):
    #用户名
    nickname: str = Field(..., description="用户名")