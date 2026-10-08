from fastapi import FastAPI

app = FastAPI()

# 注册子路由
from zuoye.controller.UsersController import users_router
app.include_router(users_router, prefix="/users", tags=["users"])

# 启动服务器的配置
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
        reload=False,
    )