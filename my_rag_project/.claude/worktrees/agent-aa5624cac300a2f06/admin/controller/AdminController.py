'''
    管理员的路由
'''

from fastapi import APIRouter,Depends
from admin.service import  AdminService
from admin.entity.AdminEntity import CreateUsersEntity,AdminEntity
from common.JWTUtil import token_check
admin_router = APIRouter()

#创建用户  current_user:str =Depends(token_check("admin"))表示身份为admin时允许操作
@admin_router.post("/createUsers")
def create_users(create_users_entity:CreateUsersEntity,current_user:str =Depends(token_check("admin"))):
    return AdminService.create_users(create_users_entity.email,create_users_entity.nickname)

#初始化用户密码 current_user:str =Depends(token_check("admin"))表示身份为admin时允许操作
@admin_router.post("/initPassword")
def password_init_by_nickname(admin_entity:AdminEntity,current_user:str =Depends(token_check("admin"))):
    return AdminService.password_init(admin_entity.nickname)

#删除用户 current_user:str =Depends(token_check("admin"))表示身份为admin时允许操作
@admin_router.post("/deleteUsers")
def delete_users(admin_entity:AdminEntity,current_user:dict =Depends(token_check("admin"))):
    return AdminService.delete_users(admin_entity.nickname)