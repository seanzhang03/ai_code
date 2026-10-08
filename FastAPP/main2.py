#Pydantic模型：FastAPI服务器的核心依赖，用于数据检验和序列化生成(JSON)，使用python类型提示来定义模型
#作用：数据检验、数据类型转换、自动生成文档
#在main2.py中定义一个模型（这个模型一般定义在schemas文件中）
from fastapi import FastAPI
from pydantic import BaseModel


#定义模型，定义一个Python类，在类中继承BaseModel类
class Item(BaseModel):
    name:str  #商品名称
    price:float  #价格
    description:str #商品描述
    num:int     #商品数量
    tax:float|None = None #税
    colors: list[str] = ["黑色","白色","蓝色","黄色"]       
app = FastAPI()

@app.post("/item")
async def get_item(item:Item):  #使用BaseModel定义的pydantic模型接收前端传到后端的数据，将接收到的值
    #FastAPI会自动进行数据校验，将校验后的值赋值给Item
    return item

#使用模型传输值，前端用JSON数据来传输

#访问和操作模型变量
@app.post("/create")
async def  create_item(item:Item):
    #访问模型变量时，通过变量.模型变量获取某个值
    na = item.name
    print(na)
    desc = item.description
    print(desc)
    #将前端序列转换为字典
    dict1 = item.model_dump()
    print(dict1)
    #将前端序列转换为JSON数据(字符串)
    json1 = item.model_dump_json()
    print(json1)
    return{"商品名称":na,"描述":desc}


#