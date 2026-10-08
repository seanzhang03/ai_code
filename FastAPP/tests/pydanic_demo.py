# Pydantic 作为类型提示
#Pydantic是一个库，执行数据检验，将数据变量声明为有数据类型的变量，在传参的时候，pydantic会自动执行数据类型检测，将其他数据类型转换为定义好的数据类型，并将值赋值给对应变量
#第一步，导入Pydantic库
from pydantic import BaseModel #将Pydantic导入进来，进行数据检验
from datetime import datetime
from typing import List

#使用class修改一个python类(User)
class User(BaseModel):  #继承了BaseModel，获得所有数据验证和序列化的能力
    id:int
    username:str
    birthday:datetime | None = None  #None = None表示这个属性是一个可选属性，如果没使用None，就认为这个属性是必选属性
    hobby:  List[str] = []  #小写不需要导入包，大写要导入 ，[]表示列表值为空

exex_user = {  #字典
    "id" : "20220101",  #Pydantic会检查传入的数据类型是否匹配，将字符串自动转换为int类型    
    "username" : "zhangsan",
    "birthday" : "2000-01-01 12:00",  #自动转换为datetime对象
    "hobby" : ["1","唱","跳","rap","篮球"]
}

#创建一个对象User，Pydantic会自动将字典的值，通过key转换为对象的属性、变量值，eg将id这个key转换为变量id
user = User(**exex_user)  #要加**来进行字典解包，不然Pydantic的BaseModel在实例化时不能直接传入一个字典作为位置参数
print(user)

#扩展（可变参数）
print("==========")#### 序列解包 
first,*second,third = [1,3,5,6,7,8,9,10]  #先将没有*的变量赋值，然后将剩下变量给有*的
print(first)
print(second)
print(third)
#一个变量接收一个值，多余变量值一般用*变量接收（一般称为解包）
#*可变参数可以接收多个值

def info(**kwargs:str):  #**解析字典
    print(kwargs)
info(username="zhangsan",age="20",school="北大")
info(name="lisi",phone="12345")  #能接受不一样的数据，**也表示接收可变参数，传的值不确定有多少个

def user_info(name:str,age:int,school:str):
    print(f"我是{name}，今年{age}岁，就读于{school}")
user={"name":"wangwu","age":"22","school":"清华"}
user_info(**user)
dict1 ={"a":"zhangsan","b":"lisi","c":"wangwu"}
dict2 = {"c":"hello","d":"world"}
dict3 = {**dict1,**dict2}  #dict2将dict1里面的c覆盖掉了
print(dict3)

#元数据注解类型提示