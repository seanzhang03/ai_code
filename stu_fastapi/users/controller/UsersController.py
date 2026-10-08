#用来控制配置路由访问
import json

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from users.entity.LoginUsers import LoginUsers
from users.service import UsersService

# 子路由配置，将用户模块的所有接口(发送验证码、注册、登录等)都挂载在一个users_router下，代码结构更清晰
users_router = APIRouter()#所有用户的接口都注册到该路由器上

# 发送验证码路由配置
@users_router.get("/sendCaptcha") #告诉FastAPI，这是GET请求，路径为/sendCaptcha，该接口属于users_router这个路由器
def send_captcha(email: str):
    return UsersService.send_captcha(email) #调用服务层的send_captcha方法，传入email，将返回的结果直接作为HTTP响应返回给客户端

# 登录路由配置
@users_router.post("/login")
def login(user:LoginUsers): #entity里类的实例化对象
    return UsersService.login(user.email,user.captcha)


# #聊天路由配置
# @users_router.get("/chat")
# def chat(question):
#     print(question)
#     def generator():
#
#         for item in range(10):  #控制流式输出次数
#             yield f"data:{json.dumps({"content":str(item)})}\n\n"  #sse数据相应的格式，如果用的是fetch直接写str(item)即可
#         yield f"data:{json.dumps({"content":"[DONE]"})}\n\n"  #[DONE]表示结束
#     return StreamingResponse(
#         content = generator(),
#         media_type="text/event-stream" #声明响应的MIME类型为text/event-stream，告诉客户端这是一条SSE流，按事件流方式持续读取，而非当成普通一次性响应
#     )