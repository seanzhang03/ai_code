"""
    定义在各个模型下的接口，是我们的子路由来定义请求路径的
    子路由定义的请求路径如果想要真正意义上发生作用，需要在main.py通过fastapi对象注册
"""
from time import sleep

# 导入子路由类
from fastapi import APIRouter, Header

# 创建子路由对象
stu_router = APIRouter()

# 通过子路由对象定义一个接口函数
"""
    @stu_router：使用子路由对象定义一个接口
    get("/say")：定义接口的请求方式为get，接口的请求路径为say，完整的请求路径--http://localhost:8000/stu/say
"""


@stu_router.get("/say")
def say():
    return {"msg": "今天天气还不错"}


# post 请求
@stu_router.post("/say2")
def say2():
    return {"msg": "今天天气还不错"}


"""
    无论是get请求、post请求，这个函数中常用的参数有哪些
    @stu_router.get(
        path="/say3", # 请求路径
        description="
            接口描述：比如这个接口做了什么事情
        ",
    )
"""

"""
    get 请求中，客户端如何提交数据内容给服务器
    案例：用户在执行登录操作的时候，为了验证用户输入的账号和密码是否能够通过认证，从而执行登录，那么
        就需要拿到用户输入的账号和密码进行验证
    常见的方案：
        1、URL中，以键值对的格式拼接传递
        2、URL中，以路径参数的形式传递
"""


# 1、URL中，以键值对的格式拼接传递
@stu_router.get("/login1")
def login1(username: str, password: str):
    print(f"接收到的账号和密码分别为：{username}, {password}")
    # 省略判断 --- 假设判断通过
    return {
        "code": 200,  # code：请求后的状态码，200成功，500代码有问题，不同的数值表示不同的意思
        "msg": "登录成功",  # msg：提示信息
        "data": None,  # data：数据内容，没有就None
    }


# 2、URL中，以路径参数的形式传递
@stu_router.get("/login2/{username}/{password}")
def login2(username: str, password: str):
    print(f"接收到的账号和密码分别为：{username}, {password}")
    # 省略判断 --- 假设判断通过
    return {
        "code": 200,  # code：请求后的状态码，200成功，500代码有问题，不同的数值表示不同的意思
        "msg": "登录成功",  # msg：提示信息
        "data": None,  # data：数据内容，没有就None
    }


"""
    post 请求中，客户端如何提交数据内容给服务器
    常见方案：
        1、把参数放在请求体里面 --- 放JSON对象
    即：客户端在传递数据给服务器的时候，需要把数据内容转换为json对象，然后在传递
    接收json数据的时候，需要定义一个类，类的属性就和json对象的key相同，然后用类的对象来接收数据
"""
from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    # 变量名:类型 = Field(..., description="字段描述")
    username: str = Field(..., description="账号")
    password: str = Field(..., description="密码")


@stu_router.post("/login3")
def login3(userLogin: UserLogin):
    print(userLogin)
    # 省略判断 --- 假设判断通过
    return {
        "code": 200,  # code：请求后的状态码，200成功，500代码有问题，不同的数值表示不同的意思
        "msg": "登录成功",  # msg：提示信息
        "data": None,  # data：数据内容，没有就None
    }


"""
    定义一个接收客户端传过来的文件的接口 --- 这个接口的请求方式必须是 post
"""
from fastapi import File, UploadFile, Form


@stu_router.post("/uploadFile")
# file: UploadFile = File(...)：表示使用UploadFile类来接收文件、file就是对象的名字【客户端传递文件的时候也设置为file】
# userId: int = Form(...)：表示使用Form类来接收表单数据、userId就是对象的名字【客户端传递表单数据的时候也设置为userId】
def upload_file(file: UploadFile = File(...), userId: int = Form(...)):
    print(userId)
    """
        把文件存储在根目录下的/static/files中
    """
    # 以当前时间戳转为整数后作为文件名字
    import time
    filename = str(int(time.time())) + "." + file.filename.split(".")[-1]
    with open(r"E:\workspace\feifan_three\stu_fastapi\static\files\\" + filename, "wb") as f:
        # file.file.read()：读取文件内容
        f.write(file.file.read())
    return {
        "code": 200,
        "msg": "上传成功",
        "data": None
    }


# 返回数据就是一个str
@stu_router.get("/getStr")
def get_str():
    return "hello world"


# 流式输出
from starlette.responses import StreamingResponse


@stu_router.get("/stream")
def stream():
    # 定义一个函数，通过yield返回一个可迭代对象，提供给content使用
    # 本质上yield返回的内容就是每一次输出【本次项目中就是llm】的结果
    def generator():
        for item in range(1000):
            sleep(1)
            yield str(item)

    return StreamingResponse(
        content=generator(),  # content的值是一个可迭代的对象，通过yield实现
        # text/plain：表示返回数据的媒体类型为纯文本
        # text/event-stream：表示返回数据的媒体类型为事件流 -- 实时响应
        media_type="text/event-stream",  # 媒体类型，这个参数根据自己业务去查对应值
    )

class EmailLogin(BaseModel):
    email:str = Field(...,description="邮箱")
    password:str = Field(...,description="密码")

#学习jwt的登录
@stu_router.post("/login")
def login(user:EmailLogin):
    print(user)
    #省略进行账号密码的比对，直接输出登录成功
    #生成token
    from stu.utils.JwtUtil import create_token
    #字典中的内容就是想要存入token的数据内容--必须要的信息
    token = create_token({"email":user.email,"roleName":"admin"})
    print(token)
    return {
        "code":200,
        "msg":"登录成功",
        "data":token
    }

#获取token的信息
@stu_router.get("/tokenget")
def me(Authorization:str = Header(None)):#header通过参数获取这个请求头的信息---这样写就是进入接口后自己处理
    print(Authorization)
    return{
        "code":200,
        "msg":"登录成功",
        "data":Authorization

    }
from fastapi import Depends
from stu.utils.JwtUtil import get_current_user

#使用fastapi提供的Depends来实现token认证
@stu_router.get("/tokenauth")
def me(user_info:dict =Depends(get_current_user)):
    print(f"me方法执行了{user_info}")
    return {
        "code":200,
        "msg":"获取成功",
        "data":"aaa"
    }

#查询用户信息
@stu_router.get("/usersList")
def users_list(current_user:str=Depends(get_current_user)):
    print(current_user)
    return {
        "code":200,
        "msg":"获取成功",
        "data":[
            {"name":"zhangsan","age":18},
            {"name":"lisi","age":19},
            {"name":"wangwu","age":20},
        ]
    }

#删除用户
from stu.utils.JwtUtil import token_check
@stu_router.delete("/deleteUsers")
def delete_users(
        current_user:str =Depends(token_check("admin"))
):
    print(current_user)
    return {
        "code":200,
        "msg":"删除成功",
        "data":None
    }

'''
"""
    定义在各个模型下的接口，是我们的子路由来定义请求路径的
    子路由定义的请求路径如果想要真正意义上发生作用，需要在main.py通过fastapi对象注册
"""
from time import sleep

# 导入子路由类
from fastapi import APIRouter

# 创建子路由对象
stu_router = APIRouter()

# 通过子路由对象定义一个接口函数
"""
    @stu_router：使用子路由对象定义一个接口
    get("/say")：定义接口的请求方式为get，接口的请求路径为say，完整的请求路径--http://localhost:8000/stu/say
"""


@stu_router.get("/say")
def say():
    return {"msg": "今天天气还不错"}


# post 请求
@stu_router.post("/say2")
def say2():
    return {"msg": "今天天气还不错"}


"""
    无论是get请求、post请求，这个函数中常用的参数有哪些
    @stu_router.get(
        path="/say3", # 请求路径
        description="
            接口描述：比如这个接口做了什么事情
        ",
    )
"""

"""
    get 请求中，客户端如何提交数据内容给服务器
    案例：用户在执行登录操作的时候，为了验证用户输入的账号和密码是否能够通过认证，从而执行登录，那么
        就需要拿到用户输入的账号和密码进行验证
    常见的方案：
        1、URL中，以键值对的格式拼接传递
        2、URL中，以路径参数的形式传递
"""


# 1、URL中，以键值对的格式拼接传递
@stu_router.get("/login1")
def login1(username: str, password: str):
    print(f"接收到的账号和密码分别为：{username}, {password}")
    # 省略判断 --- 假设判断通过
    return {
        "code": 200,  # code：请求后的状态码，200成功，500代码有问题，不同的数值表示不同的意思
        "msg": "登录成功",  # msg：提示信息
        "data": None,  # data：数据内容，没有就None
    }


# 2、URL中，以路径参数的形式传递
@stu_router.get("/login2/{username}/{password}")
def login2(username: str, password: str):
    print(f"接收到的账号和密码分别为：{username}, {password}")
    # 省略判断 --- 假设判断通过
    return {
        "code": 200,  # code：请求后的状态码，200成功，500代码有问题，不同的数值表示不同的意思
        "msg": "登录成功",  # msg：提示信息
        "data": None,  # data：数据内容，没有就None
    }


"""
    post 请求中，客户端如何提交数据内容给服务器
    常见方案：
        1、把参数放在请求体里面 --- 放JSON对象
    即：客户端在传递数据给服务器的时候，需要把数据内容转换为json对象，然后在传递
    接收json数据的时候，需要定义一个类，类的属性就和json对象的key相同，然后用类的对象来接收数据
"""
from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    # 变量名:类型 = Field(..., description="字段描述")
    username: str = Field(..., description="账号")
    password: str = Field(..., description="密码")


@stu_router.post("/login3")
def login3(userLogin: UserLogin):
    print(userLogin)
    # 省略判断 --- 假设判断通过
    return {
        "code": 200,  # code：请求后的状态码，200成功，500代码有问题，不同的数值表示不同的意思
        "msg": "登录成功",  # msg：提示信息
        "data": None,  # data：数据内容，没有就None
    }


"""
    定义一个接收客户端传过来的文件的接口 --- 这个接口的请求方式必须是 post
"""
from fastapi import File, UploadFile, Form


@stu_router.post("/uploadFile")
# file: UploadFile = File(...)：表示使用UploadFile类来接收文件、file就是对象的名字【客户端传递文件的时候也设置为file】
# userId: int = Form(...)：表示使用Form类来接收表单数据、userId就是对象的名字【客户端传递表单数据的时候也设置为userId】
def upload_file(file: UploadFile = File(...), userId: int = Form(...)):
    print(userId)
    """
        把文件存储在根目录下的/static/files中
    """
    # 以当前时间戳转为整数后作为文件名字
    import time
    filename = str(int(time.time())) + "." + file.filename.split(".")[-1]
    with open(r"E:\workspace\feifan_three\stu_fastapi\static\files\\" + filename, "wb") as f:
        # file.file.read()：读取文件内容
        f.write(file.file.read())
    return {
        "code": 200,
        "msg": "上传成功",
        "data": None
    }


# 返回数据就是一个str
@stu_router.get("/getStr")
def get_str():
    return "hello world"


# 流式输出
from starlette.responses import StreamingResponse


@stu_router.get("/stream")
def stream():
    # 定义一个函数，通过yield返回一个可迭代对象，提供给content使用
    # 本质上yield返回的内容就是每一次输出【本次项目中就是llm】的结果
    def generator():
        for item in range(1000):
            sleep(1)
            yield str(item)

    # StreamingResponse：流式输出
    return StreamingResponse(
        content=generator(),  # content的值是一个可迭代的对象，通过yield实现
        # text/plain：表示返回数据的媒体类型为纯文本
        # text/event-stream：表示返回数据的媒体类型为事件流 -- 实时响应
        media_type="text/event-stream",  # 媒体类型，这个参数根据自己业务去查对应值
    )


# 聊天
from fastapi import Request
from stu.service import StuService

@stu_router.get("/chat")
def chat(question: str, request: Request):
    # 取出初始化的对象
    load_model = request.app.state.load_model
    return StreamingResponse(
        content=StuService.chat(question, load_model),
        media_type="text/event-stream",
    )

'''