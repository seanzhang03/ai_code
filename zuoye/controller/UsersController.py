from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from zuoye.service import UsersService

# 子路由
users_router = APIRouter()

# 定义请求体模型
class LoginRequest(BaseModel):
    email: str
    code: str

# 发送验证码
@users_router.get("/sendCaptcha")
def send_captcha(email: str):
    return UsersService.send_captcha(email)

# 验证码登录
@users_router.post("/login")
def login(login_req: LoginRequest):
    return UsersService.login(login_req.email, login_req.code)