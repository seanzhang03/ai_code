from fastapi import FastAPI

app = FastAPI()

#跨域配置，实际上就是方便后端将响应数据传给前端
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:8080"], #允许所有来源，这里不能用*，[]里是前端的协议，ip和端口
                                               #注意这里有没有/都很关键，前端访问的ip地址必须和这里一模一样
    allow_credentials=True,
    allow_methods = ["*"], #允许所有方法
    allow_headers = ["*"], #允许所有头
)

#注册子路由
from stu.controller.StuController import stu_router
#app.include_router:注册子路由，参数如下：
#1.router：子路由对象--通过APIRouter创建出来的
#2.prefix：子路由的前缀--访问子路由的接口的时候默认加上路径
    #3.tags：子路由的标签-SwaggerUI中用来分组的，一个标识，便于查看
app.include_router(stu_router,prefix="/stu",tags=["stu"])
from users.controller.UsersController import users_router
app.include_router(users_router,prefix="/users",tags=["users"])
from chat.controller.ChatController import chat_router
app.include_router(chat_router,prefix="/chat",tags=["chat"])
from history.controller.HistoryController import history_router
app.include_router(history_router,prefix="/history",tags=["history"])

#启动服务器的配置
if __name__ == "__main__":
    import uvicorn
    #通过uvicorn运行FastAPI应用
    uvicorn.run(
        app,  #FastAPI应用实例
        host = "localhost",  #服务器地址
        port = 8000,  #服务器端口
        reload = False,  #修改代码后不自动更新
    )



##################################################
'''


    from fastapi import FastAPI

"""
    fastapi的生命周期：
        在启动服务器的时候执行一些代码【初始化代码】
        关闭服务器的时候执行一些代码【清除对象代码】
"""
from contextlib import asynccontextmanager
from common.LoadLLMModel import LoadLLMModel
@asynccontextmanager
async def lifespan(app: FastAPI):
    # yield之前的代码在启动项目的时候就执行了
    # 可以把创建出来的内容存入到app.state中，格式：app.state.名字 = 值
    # 取值方式：在接口中通过请求对象request实现，格式：request.app.state.名字
    app.state.load_model = LoadLLMModel()    # 启动的时候构建加载模型的对象
    print("成功加载了各个模型对象")
    yield
    # yield之后的代码在关闭项目的时候就执行了
    del app.state.load_model
    print("成功清除了各个模型对象")
app = FastAPI(lifespan=lifespan)

# 注册子路由
from stu.controller.StuController import stu_router
"""
    app.include_router：注册子路由，参数如下：
        1、router：子路由对象 --- 通过APIRouter创建出来的
        2、prefix：子路由的前缀 --- 访问子路由的接口的时候默认加上这个路径
        3、tags：子路由的标签 --- SwaggerUI中用来分组的，一个标识，便于查看
"""
app.include_router(stu_router, prefix="/stu", tags=["stu"])


# 启动服务器的配置
if __name__ == '__main__':
    import uvicorn

    # 通过uvicorn运行FastAPI应用
    uvicorn.run(
        app,  # FastAPI应用实例
        host="localhost",  # 服务器地址
        port=8000,  # 服务器端口
        reload=False,  # 修改代码后不自动更新
    )

'''

