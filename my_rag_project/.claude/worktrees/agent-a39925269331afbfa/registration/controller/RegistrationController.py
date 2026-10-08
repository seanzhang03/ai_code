'''
    该模块是账号注册的路由配置
'''

from fastapi import APIRouter
from registration.entity.RegistrationEntity import RegistrationEntity
from registration.service import RegistrationService
#子路由配置：配置注册接口
registration_router = APIRouter()

#注册账号路由配置
@registration_router.post("/registration")
def registration(registration_entity:RegistrationEntity):
    return RegistrationService.registration(registration_entity.email,registration_entity.password,registration_entity.nickname)