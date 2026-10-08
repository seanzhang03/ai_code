#python遇到错误的代码或者我无法正常处理程序就会产生一个异常（bug）并抛出
#异常被抛出后，可以被捕捉，捕捉后程序会按照某种机制继续运行，如果对抛出的异常不做任何处理的话，那么程序就会终止运行
#把错误的异常也给封装成了类
#捕获单个异常的格式：
#try:
#有可能发生异常的代码
#except:  捕获多个异常就在单个异常的名字改为多个就行
#异常发生后要执行的代码
#else:（可选）
#如果没有异常发生，在try执行后执行这里的代码
#finally:（可选）
#不管有没有捕获到异常，最后都会执行这里的代码   
#异常的传递性：
#当一个函数或方法抛出一个异常时，这个异常会被传递到调用者那里，如果调用者没有捕获异常的话，那么程序会终止

#自定义异常
#在python中，用raise关键字来手动抛出异常，其格式为：raise Exception (arg)
#Exception用于指定要抛出的异常类型，该类型来自于python解释器自带的异常类型
#arg是一个可选的参数，更多的用于提供关于异常的信息
#在python中，除了已有的异常类型之外，还可以自己定义自己的异常类型，但是必须继承Exception类
'''
import time
#KeyboardInterupt，手动终止程序
for i in range(100):
    print(i)
    time.sleep(1)
'''
'''
#AttributeError:尝试访问对象所没有的属性时爆发
my_str = 'abcdef'
my_str.abc()
'''
'''
#IndexError：访问不存在的索引时会触发
my_list = [1,2,3]
print(my_list[5])
'''

#捕获单个异常
try:
    x=10
    y=0
    print(x/y)
except ZeroDivisionError:
    print("除数不能为0")
else:
    print("代码正常运行，没有触发异常")
finally:
    print("不管有没有触发异常，我都会执行")

#捕获所有的异常
try:
    x=10
    y=0
    z=x/y
except Exception as e:
    print(e)

#用raise关键字手动抛出异常终止程序
#raise NameError("手动抛出的某某异常")

#自定义异常
class MyException(Exception):
    def __init__(self,message,error_code,traceback=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
#raise MyException("某某某出问题了",100)
        