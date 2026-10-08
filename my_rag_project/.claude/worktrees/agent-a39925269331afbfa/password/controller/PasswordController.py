'''
    本模块是用户实现密码修改的数据库操作的路由挂载
'''

from fastapi import APIRouter
from password.service import PasswordService
from password.entity.PasswordEntity import ChangePasswordCaptchaEntity,ChangePasswordPasswordEntity
password_router = APIRouter()

#修改密码发送验证码
@password_router.get("/sendCaptcha")
def send_captcha_for_password_change(email):
    return PasswordService.send_captcha_for_password_change(email)

#通过旧密码修改密码
@password_router.post("/changePasswordPassword")
def change_password_by_password(change_password_password_entity:ChangePasswordPasswordEntity):
    return PasswordService.change_password_by_password(
        change_password_password_entity.email,
        change_password_password_entity.old_password,
        change_password_password_entity.new_password
        )

#通过验证码修改密码
@password_router.post("/changePasswordCaptcha")
def change_password_by_captcha(change_password_captcha_entity:ChangePasswordCaptchaEntity):
    return PasswordService.change_password_by_captcha(
        change_password_captcha_entity.email,
        change_password_captcha_entity.captcha,
        change_password_captcha_entity.new_password,
        )