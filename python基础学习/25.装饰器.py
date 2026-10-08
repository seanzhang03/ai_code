#装饰器本质上是一种特殊的嵌套函数，接受一个函数作为参数（该函数为被装饰的函数），并返回一个新的函数（装饰之后的函数）
#装饰器最大的作用即 不改变装饰函数代码的情况下去添加新功能
def decorator(f):
    def f1():
        print("b")
        f()
        print("c")
    return f1

def func():
    print("a")

func = decorator(func)
func()

#语法糖：编程语言提供的，可以让代码更简洁易于理解和书写的语法特性，这些特性不带来新功能，但使代码更易于阅读和维护
#装饰器的语法糖：
#下面和func = decorator(func)等效
@decorator
def func():
    print("a")

#上面的装饰带参数的函数是指被装饰的函数带参数，而这里的带参数的装饰器是指装饰器本身需要参数，而装饰器本身又要接受被装饰的函数名称，并返回一个新函数
#故为了保证装饰器能顺利接受参数及顺利接受被装饰的函数，需要在装饰器内部多一层内嵌函数，最外层的函数用来获取装饰器参数
#中间的函数用来获取被装饰的函数名称，最内层的函数负责功能添加
def func1(prefix):
    def decorator(func):
        def wrapper(*args,**kwargs):
            result= func(*args,**kwargs)
            return f"{result}{prefix}"
        return wrapper
    return decorator

#使用装饰器并传递参数
@func1("How are you?")  #直接使用装饰器语法糖要将其写在被装饰的函数定义上面
def greet(name):
    return f"Hello,{name}."
#greet=func1("How are you?")(greet)
print(greet("Alice"))
#greet=func1("How are you?")(greet)等同于@func1("How are you?")
#先将"How are you?"传到prefix，greet=func1("How are you?")(greet)变为greet=decorator(greet)
#然后变为greet = decorator

#装饰器嵌套：一个函数可以被多个装饰器依次装饰，每个装饰器都会对原始函数进行一层包装
#从而在调用原始函数时，可以依次执行每个装饰器中的逻辑，以达到为该函数添加多个不同功能的需求
#装饰器嵌套时，执行顺序是从下到上，且最下面的装饰器的返回值返回给上一层的装饰器作为参数，然后层层传递直到最上面的装饰器
#当我们要运行被装饰的函数时，相当于从最上层的装饰器开始向下运行直到运行完毕
def decorator_one(func):
    def wrapper_one(*args,**kwargs):
        print("Decorator one - before call")
        result = func(*args,**kwargs)
        print("Decorator one - after call")
        return result
    return wrapper_one

def decorator_two(func):
    def wrapper_two(*args,**kwargs):
        print("Decorator two - before call")
        result = func(*args,**kwargs)
        print("Decorator two - after call")
        return result
    return wrapper_two
@decorator_one
@decorator_two
def say_hello(name):  #先将参数传给装饰器二，再传给参数一，然后从上到下进行装饰，最后返回
    print(f"Hello,{name}")
say_hello("Alice")
#整体流程：say_hello调用流程，先将say_hello传递给decorator_two，返回一个wrapper_two,再将wrapper_two作为参数传递给decorator_one
#然后返回wrapper_one，即say_hello(name)被修饰成了wrapper_one(name)，然后wrapper_one(name)中result调用了形参func，这里的func是装饰器而返回的wrapper_two函数
#然后进入wrapper_two的函数体里面，wrapper_two函数再调用result里的func，这里的func即say_hello,调用完后返回wrapper_two到wrapper_one里的result，然后warpper_one执行完毕后
#返回一个wrapper_one到say_hello，执行完毕

#类装饰器：除了定义一个新函数用作装饰器外，还可以将一个类作为装饰器，给被装饰的函数添加新的功能
#类装饰器通过实现类的__call__方法，来使得类的实例可被当作函数来调用，从而实现对其他函数的装饰
class MyDecorator:
    def __init__(self,func):
        self.func=func
    def __call__(self,*args,**kwargs):
        print("Something is happening before the function is called")
        result = self.func(*args,**kwargs)
        print("Something is happening after the function is called")
        return result
@MyDecorator
def say_hello(name):
    print(f"Hello,{name}")
say_hello("Alice")

import logging
def log_decorator(func):
    def wrapper(*args,**kwargs):
        logging.basicConfig(filename='./app.log',level=logging.INFO,filemode='a',format='%(name)s-%(levelname)s-%(asctime)s-%(message)s')
        logging.warning(f"Calling function:{func.__name__} with args:{args} and kwargs:{kwargs}")
        result = func(*args,**kwargs)
        logging.warning(f"Function {func.__name__} returned:{result}")
        return result
    return wrapper

@log_decorator
def test():
    print("123")
test()