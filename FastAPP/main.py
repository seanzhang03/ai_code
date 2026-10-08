from fastapi import FastAPI



'''
#创建fastapi服务器对象
app = FastAPI()
#定义一个接口方法，用于前端用户访问的接口
#FastAPI服务器，支持异步请求，可以同时运行多个程序，当一个程序暂停时，fastapi会转而执行其他程序，get("/")表示改方法的请求地址和路径
@app.get("/")  #通过app就是fastapi服务器对象，将我们定义的方法，暴露出去，get()表示请求方法
async def root():  #async异步请求，用来定义异步请求方法，一般搭配wait一起使用，用它修饰方法表示这个方法是一个异步请求方法，
    #当这个方法因为线程阻塞时方法暂时停止运行时，它会执行其他方法而不会浪费时间
    return {"message":[{"role":"user","content":"你好，我是第一个FastAPI程序"}]}

if __name__ == "__main__":
    import uvicorn #ASGI服务器，通常用来运动fastapi
    uvicorn.run(app,host="127.0.0.1",port=8000) #使用uvicorn ASGI代理，运行fastapi项目，请求地址，port 服务器端口号
    #FastAPI技术栈
    # startlette：fastapi的Web层，提供路由和中间件等基础框架，FastAPI服务器直接继承Startlette
    #Pydantic：数据检验层，提供数据检验，基于Python类型提示自动生成API文档，序列生成、数据检验
    #Uvicorn：AGSI服务层，基于uvloops和httptools高性能服务器，用于运行FastAPI项目/服务器
    #fastapi服务器自动生成的API文档：运行对应ip地址和端口后，加上后缀，如http://127.0.0.1:8000/docs#
    #前端页面发送axios请求给网络代理，再通过找到API接口进行查询数据库、调用其他端口，然后查找对应中间件，若中间件没有数据会去MySQL数据库找数据，找到数据之后数据库会将数据发送到端口，端口通过方法访问，将数据库里的数据返回给网络代理，最后再渲染到浏览器
    #使用命令行运行fastapi服务器： uvicorn main:app --reload  要转到当前文件夹下
    #http://127.0.0.1:8000/redoc 专门阅读端口 
    #访问fastapi自动生成的api文档(Swagger UI页面，可以将进行API交互)http://127.0.0.1:8000/docs#
    #访问fastapi ReDoc，注重文档阅读，无法进行API交互
    # 浏览器请求方法和装饰器方法
    #FastAPI服务器这只是的HTTP协议方法
    #@app.get("/请求路径") 表示这是一个HTTP协议的GET请求，一般用于获取、读取数据
    #app.post("/请求路径") 这是一个HTTP协议的post 请求方式，一般用于创建新的数据
    #app.delete("/请求路径") 这是HTTP协议的delete请求方式，一般般用于删除数据
    #app.put("/请求路径")这是一个HTTP协议的put请求，一般用于更新数据
    #app.patch("/请求路径")这是一个HTTP协议的patch请求，一般用于更新部分数据

    #python类型提示
    #python支持可选的类型提示功能，也能被称为类型注解：用来声明变量的数据类型，达到一个提示的作用
    #动机(没有类型声明)在FastAPP中，新建一个Python Package -->(tests)
'''



'''
from fastapi import FastAPI
app = FastAPI()
from typing import Annotated
@app.get("/name")
async def say_hello(name:Annotated[str,"this is username"]):  #说明作用
    return f"Hello {name}"

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app,host="127.0.0.1",port=8000) 
'''





from fastapi import FastAPI
app = FastAPI(
    title = "我是FastAPI测试接口",  #fastapi服务器的名称
    version = "1.0.0",  #API接口的版本信息号
    description = "这是一个API测试接口",  #API接口描述信息
    terms_of_service = "www.baidu.com",  #服务条款接口URL
    contact = {
        "name":"自己的名字",
        "url":"https://empaltes.com",
        "email":"1607259232@qq.com"
    },
    license_info = {  #软件许可证信息
        "name":"MTH",
        "url":"https://emap.com"
    }
)
from typing import Annotated
@app.get("/name")
async def say_hello(name:Annotated[str,"this is username"]):  #说明作用
    return f"Hello {name}"

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app,host="127.0.0.1",port=8000) 