#为API请求地址/路由/路径添加文档信息
from fastapi import FastAPI

app = FastAPI(
    title = "商品服务器项目",
    version = "1.1.0",
    description="这是一个管理商品的fastapi服务器"
)
@app.post(
    "/add", #请求地址/路由/路径
    summary = "添加商品的API",  #定义api接口的摘要信息
    description = "这是商品的添加API接口，添加商品ID item_id，商品名称 ",  #定义api接口的描述信息，比如变量名称和对应的名字
    tags = ["商品管理"] , #api接口的分类信息
    response_description="返回商品ID和商品名称",  #返回值/响应信息
        )
async def read_item(item_id:int,name:str) -> dict:
    return {"item_id":item_id,"name":name}  #构建字典返回字典

@app.post(
    path = "/user",  #请求路径(静态路径)
    summary="添加用户的api接口",
    tags=["用户管理"]
)
async def user_item(username:str,phone:str,email:str) ->dict:
    return {"username":username,"phone":phone,"email":email}

@app.get(path = "/user/{name}",tags=["用户管理"])  #动态路径 ，使用形参变量作为路径地址，比如/user/{name}，name和形参变量name:str是同一个
async def get_item(name:str|None = None) ->dict:
    return [{"name":name},{"name":"lisi"},{"name":"wawngwu"}]
#动态路径的请求方法(Restful): 127.0.0.1:8000/user/xiaohua/123456789  将参数拼接到路由地址中
#静态路由的请求方式: 127.0.0.1:8000/user/?username=xiaohua&phone=1899091123&email=26374623%40qq.com
#在fastapi中，推荐使用动态路径请求方法