'''
    该模块是用户登录的路由配置
'''
from fastapi import APIRouter
from login.service import LoginService
from login.entity.LoginEntity import LoginCaptchaEntity,LoginEmailPasswordEntity,LoginNicknamePasswordEntity
#子路由配置，将用户的所有接口，都挂载在login_router下
login_router = APIRouter()  #所有用户接口注册在该路由上

#发送验证码路由配置
@login_router.get("/sendCaptcha")
def send_captcha(email:str):
    return LoginService.send_captcha(email)

#邮箱验证码登录路由配置
@login_router.post("/loginByEmailCaptcha")
def login_by_email_captcha(login_captcha_entity:LoginCaptchaEntity):  #user是包含邮箱和验证码信息的LoginUsers类的一个实例对象
    return LoginService.login_by_email_captcha(login_captcha_entity.email,login_captcha_entity.captcha)

#邮箱密码登录路由配置
@login_router.post("/loginByEmailPassword")
def login_by_email_password(login_email_password_entity:LoginEmailPasswordEntity):
    return LoginService.login_by_email_password(login_email_password_entity.email,login_email_password_entity.password)

#用户名密码登录路由配置
@login_router.post("/loginByNicknamePassword")
def login_by_nickname_password(login_nickname_password_entity:LoginNicknamePasswordEntity):
    return LoginService.login_by_nickname_password(login_nickname_password_entity.nickname,login_nickname_password_entity.password)