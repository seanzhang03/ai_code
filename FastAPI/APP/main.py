#准备：在Projects 中，新建一个 FastAPI 项目，文件夹 app
#在app项目中新建一个Python Package routers，存储 路由 代码
#在app项目中新建一个Python Package services，存储 代码 的业务逻辑
#在app项目中新建一个Python Package schemas，存储 项目的 响应数据模型
#在app项目中新建一个main.py Python 文件，用来聚合路由（路由供前端 axios 请求，请求地址）
#在app项目中新建一个Python Package  models，用来写ORM持久化模型

#在models中新建一个python file 模拟数据库数据：user.py
#在services中，新建一个user_service.py，写一个创建用户的代码
#在routers中，新建一个路由文件user_router.py，写访问路由、接口地址
#在main.py中，聚合各个路由
from fastapi import FastAPI
from routers.user_router import *

#创建fastapi 服务器
app = FastAPI(
    title="用户项目服务器",
    version="1.0.0",
    description="用户服务武器，删除、添加、修改用户信息"
)

#聚合路由/注入路由 聚合user_router
#注入的是user_router中创建的路由 router = APIRouter()
app.include_router(
    router,
    prefix="/api/vi",   #url请求地址的前缀，127.0.0.1:8000/api/v1/users
    tags =["用户管理"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)