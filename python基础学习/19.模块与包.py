#模块是一个py文件
#模块的导入使用import关键字
#import 模块 
#import 模块 as 别名
#from 模块 import 子模块
#from 模块 import *
#模块内置变量，可通过dir()查看模块内置变量：
#__name__:用于确定是被直接运行还是被导入其他模块中。当一个模块被直接运行时，__name__的值是"__main__"，否则为该模块名称
#__all__：定义一个模块中的哪些变量、函数或类可以通过from module import *导入时可以用
#......
#包是一个文件夹，实际上就是一个有层次的文件目录结构，来更好的组织和管理模块。通俗来讲就是一个目录，每一个包都要有一个__init__.py文件
#该文件可以没有内容，但是要有来表明这是一个python文件

#模块的导入
#第一种方式：使用import模块直接导入
import moduleA
#调用模块A的方式为：moduleA.add()
ret = moduleA.add(4,5)
print(ret)
#第二种方式：使用import 模块 as 别名
import moduleA as mA
ret1 =mA.add(1,2)
print(ret1)

#第三种方式：使用from模块import你想要使用的内容
#除了导入之外，该模块的其他内容是不会被导入进来的
from moduleA import add
ret2 = add(1,3)
print(ret2)

from moduleA import *
ret3 = add(4,2)
print(ret3)
ret4 = sub(4,2)
print(ret4)
#ret5 = mul(4,2)  #__all__限制了传入的参数

#os模块
import os
#使用os模块来创建一个文件夹
#定义一个变量，来代表要创建的文件夹名字
folder_name = 'new_folder'
#用来检查你要创建的文件夹是否存在
if not os.path.exists(folder_name):
    #当文件夹不存在时，在if分支里创建该文件夹
    os.mkdir(folder_name)
    print(f"{folder_name}已创建成功！！")
else:
    print("该文件已存在！")

#time模块,python非硬实时，获取时间可能不准确
import time 
start = time.time()
time.sleep(1)
stop = time.time()
print(stop-start)

#random模块
import random
a = random.randint(1,10)  #伪随机
print(a)
my_list=[1,2,3,4,5]
random.shuffle(my_list) #将列表中的元素随机打乱
print(my_list)