from pydantic import BaseModel,Field
#Field：表示这是一个属性，添加属性描述，添加属性格式，起到说明作用

class UserCreate(BaseModel):
    #Field属性中...表示是一个必填属性
    username:str = Field(...,min_length=1,max_length=10,description="用户名字",examples=["zhangsan"])
    age:int = Field(...,description="用户年龄")
    phone:str = Field(...,description="用户手机")
    email:str = Field(...,description="用户邮箱",examples=["user@example.com"])
    password:str = Field(...,description="用户密码",min_length=6,max_length=50)

