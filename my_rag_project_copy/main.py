from fastapi import FastAPI

app = FastAPI()
#跨域配置，方便后端将响应数据传给前端
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  #允许所有来源，这里不能用*，[]里是前端的协议，ip和端口
    allow_credentials=True,
    allow_methods = ["*"],  #允许所有方法
    allow_headers = ["*"],  #允许所有头
)

#注册子路由
#注册模块子路由
from registration.controller.RegistrationController import registration_router
app.include_router(registration_router,prefix="/registration",tags=["registration"])
#登录模块子路由
from login.controller.LoginController import login_router
app.include_router(login_router,prefix="/login",tags=["login"])
#对话模块子路由
from chat.controller.ChatController import chat_router
app.include_router(chat_router,prefix="/chat",tags=["chat"])
#上下文历史记录模块子路由
from history.controller.HistoryController import history_router
app.include_router(history_router,prefix="/history",tags=["history"])
#管理员功能模块子路由
from admin.controller.AdminController import admin_router
app.include_router(admin_router,prefix="/admin",tags=["admin"])
#用户修改密码模块子路由
from password.controller.PasswordController import password_router
app.include_router(password_router,prefix="/password",tags=["password"])


#启动服务器配置
if __name__ =="__main__":
    import uvicorn
    uvicorn.run(
        app,  #FastAPI应用实例
        host="localhost", #服务器地址
        port= 8000, #服务器端口
        reload= False, #修改代码后不自动更新
    )