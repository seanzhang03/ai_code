from fastapi import FastAPI
from pydantic import BaseModel,EmailStr   #EmailStr检测邮箱是否合法

class User(BaseModel):
    username:str
    email:EmailStr
    alias_name:str

#创建用户时进行调用
class CreateUser(User):  #用户创建时的模型，继承基础模型User
    password:str
    phone:str

#创建一个响应模型，返回给前端用户
class UserOut(User):
    state:int
    id:int

app = FastAPI()

#response_model返回给前端的属性和属性值
@app.post("/create",response_model=UserOut) #response_model=UserOut会报错，因为输出的反应模型为UserOut但是输入时CreateUser,但是如果给id赋一个默认值，就可以正常输出
def create_user(user:CreateUser):  
    return {"id":1,"state":1001, **user.model_dump()}  #可以用作信息保护，将CreateUser中的敏感信息进行隐藏

#FastAPI是一个现代、快速、高性能API设计框架（服务器），python web开发框架，是基于python标准的类星提示设计的，使用Startleet和Pydantic设计的

#ASGI与异步编程
#ASGI：是异步服务器网关接口(Async server gateway interface),python异步程序与WEB服务器网关接口的开发标准
#同步阻塞：一个线程只能执行一次请求，同时一次只能执行一次处理（执行一个任务），如网络等待、大文件读取，I/O异常就会阻塞等待线程，而无法执行其他程序
#性能瓶颈：高并发情况下，多线程无法满足用户要求，性能不足
#协议单一：HTTP协议只支持传统请求，不支持数据双向实时通信(WebSocket)
#ASGI:执行的是异步非阻塞(async await)执行流程，使用的是异步消息传递通信方式，并发能力单线程下一次能够执行数千条请求

#异步编程：一种允许程序在等待过程中（网络延迟，IO读取大文件、查询数据库数据库执行慢等），造成线程阻塞时，它转过去执行其他方法、程序的过程
#本质是协作式多任务处理，异步编程是一个主动让出控制权（阻塞时让出控制权），通过await实现，让其他程序先执行，执行完成后再回过头执行阻塞线程
#异步编程控制权由事件循环统一调度

#HTTP状态码
#成功响应：
# 状态码     FastAPI中常量名              解析                                      使用场景
# 200        HTTP_200_OK         请求成功时，响应体包含的内容             get读取资源、put/patch更新资源，post添加数据成功
# 201        HTTP_201_CREATED    新建资源成功时相应的内容                 Post请求创建数据成功
# 202        HTTP_202_ACCEPTED   请求已被接收，但是未完成处理             邮件发送、文件发送
# 204        HTTP_204_NO_CONTENT 操作成功，无相应内容                     DELETE删除成功、PUT更新成功无需返回响应体
#重定向
# 301        HTTP_301_MOVED_     资源路径已被更新，即将废弃该资源路径，迁移到新URL地址  API废弃或域名即将更换
#            PERMANENTLY
# 302        HTTP_302_FOUND      临时重定向
#客户端错误
# 400        HTTP_400_BAD_       前端请求参数不合法     
#            REQUEST                  
# 401        HTTP_401_           权限未认证                               TOKEN认证
#            UNAUTHORIZED           
# 403        HTTP_403_FORBIDDEN  权限不足                                 会员、超级会员
# 404        HTTP_404_NOT_FOUND  查找资源不存在
# 405        HTTP_405_NOT_ALLOWED请求方法错误、不允许                      API使用app.get，前端客户端axios(post="")
# 408        HTTP_408_TIMEOUT    请求超时                                 网络加载失败或者网络不稳定
# 409        HTTP_409_CONFILICT  重复创建唯一标识                          
# 410        HTTP_410            请求资源不存在                           数据库删除数据，但是前端界面还未消失
# 413        HTTP_413            请求资源过大，超出服务器带宽
# 415        HTTP_415            提交数据不合法，提交JSON数据Content-type:application/json
# 429        HTTP_429            请求频率过快
#服务器错误
# 500        HTTP_500            服务器错误
# 503        HTTP_503            服务不可用                               后端宕机
# 504        HTTP_504            请求资源过慢、网络过慢、数据库较大加载过慢
#                                IO文件加载过慢导致请求时间超时


#案例代码
#准备：在projects中，新建一个FastAPI项目，文件夹app
#在