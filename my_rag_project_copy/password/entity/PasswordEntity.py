from pydantic import BaseModel,Field

class ChangePasswordPasswordEntity(BaseModel):
    email:str =Field(...,description="邮箱号")
    old_password:str =Field(...,description="旧密码")
    new_password:str = Field(...,description="新密码")

class ChangePasswordCaptchaEntity(BaseModel):
    email:str = Field(...,description="邮箱号")
    captcha:str = Field(...,description="验证码")
    new_password:str = Field(...,description="新密码")