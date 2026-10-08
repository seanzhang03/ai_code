#1.定义一个简单方法，来拼接姓名
def get_full_name(first_name,last_name):
    full_name = first_name.title()+" "+last_name.title()
    return full_name

def get_full_name1(first_name:str,last_name:str) -> str: #->str表示这个方法返回值是str
    full_name = first_name.title()+""+last_name.title()
    return full_name

if __name__ == "__main__":
    first = "min"
    last = "seung"
    print(get_full_name(first,last))
    first = "yun"
    last = "minseung"
    print(get_full_name1(first,last))

#2.简单类型提示
#str/int/float/bool/bytes
def get_items(name:str,age:int,height:float,state:bool,gender:bytes) -> str:
    return f"我是:{name}，今年{age}岁，身高{height}，状态{state}，性别{gender}"

if __name__ == "__main__":
    print(get_items("张三",20,160,True,b"M"))

#3.任意数据类型
#声明 数据变量 为任意数据类型
from typing import Any #表示任意数据类型（不常用）
def some_data(data:Any):
    return data

if __name__ == "__main__":
    print(some_data(True))

#4.泛型数据类型
#有些变量类型，可以在中括号内，定义数据类型，比如字符串列表，可定义为list[str]，这种在括号内定义的数据类型，就称为泛型类型或泛型
#list/set/tuple/dict
#泛型列表
#定义一个字符串列表
from typing import List
def process_item(items:list[str]):  #等同于数据结构 list
    for item in items:
        #return item  #return返回一次就结束了故要用yield
        yield item
    

if __name__ =="__main__":
    list1 = ["苹果","香蕉","桃子","李子 "]
    a = process_item(list1)  #返回的是一个生成器，生成器本质是迭代器，故要迭代来访问其中的对象
    print(a)
    for i in a:
        print(i)

#定义元组（不可变 有序 序列） 集合（可变序列）
from typing import Tuple,Set,Union
def process_tuple_set(tuples :Tuple[int,str,float,bool,str],sets: Set[Union[int,str]])->Tuple: #可添上->Any或->Tuple
    return tuples,sets

if __name__ =="__main__":
    tup = (89,"word",0.1,True,"aaa")
    sets={"world",15}
    a_tuple = process_tuple_set(tup,sets)
    for i in a_tuple[0]:
        print(i)

#定义一个字典 （可变的key:value键值对）
from typing import Dict

def process_dict(it_dict:Dict[str,int]) -> Any:
    for key,value in it_dict.items():  #items()获取字典的键和值
        yield key,value

if __name__ =="__main__":
    dict1 = {"username":123, "password":45665,"phone":12345}
    a_dict = process_dict(dict1)
    for i in a_dict:
        print(i)

#定义union个数据类型（定义若干个数据类型，比如一个变量中，存储多个数据类型 list[1,"str",89.0]）
def data_union(data:int |str |bool |float) ->List :  #联合类型，表示可以存储声明数据类型中的一个或多个类型的数据
    return data

if __name__ =="__main__":
    data = ["hello",10,False,"zhangsan"]
    print(data_union(data))

#None:表示这个存储的值可能为空
def none_data(username: str | None = None) -> str|None:  #None声明表示数据可以为空
    if username is None:
        print("string is None")
    else:
        print(username)

if __name__ =="__main__":
    none_data()
    none_data("hello")

# Pydantic 作为类型提示
#Pydantic是一个库，执行数据检验，将数据变量声明为有数据类型的变量，在传参的时候，pydantic会自动执行数据类型检测，将其他数据类型转换为定义好的数据类型，并将值赋值给对应变量
