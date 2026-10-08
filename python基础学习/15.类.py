#对象拥有类所定义的全部属性和行为
#对象的属性和行为可以单独进行增加、删除、修改
#对象不能单独创建，必须依托类的实例化，且一个类可以实例化无数的对象
#对象之间的属性和行为是不共享的
#在python中，一切皆对象
#self是一个参数，表示对象自身，里面存放着对象自身的地址，如果希望类中的方法可以被对象调用
#那么第一个参数一定是self，作用就是让实例对象与类的方法进行绑定
#这样才能让每个对象调用属于自己的方法
#构造函数__init__()：在创建对象时自动调用的一种函数，用来进行初始化属性，不是必须要定义的，可在需要时定义
#能帮我们自动修改属性
#析构函数__del__()：在对象的引用清零时自动调用，在python中不推荐使用
#类属性：类定义时所定义的属性，用来说明类本身
#实例属性：属于对象本身的属性，存在于_init_函数中，在对象创建时会赋值给该对象
#实例方法：第一个参数传入self参数，没有实例化前，无法调用，实例化后也多使用对象调用而非类调用
#静态方法：与类里的数据不共享，有自己的参数，类和对象都可以调用
#类方法：第一个参数传入cls参数，表示类本身，类和对象都可以调用，用于访问类本身的属性

#类的定义
class Person:
    name = 'ZhangSan'
    age = 20
    gender = '男'
    def eat(self):  #有self参数这个方法时想被对象调用的
        print("吃饭")
    def drink(self):
        print("喝水")
person = Person()
print(person)
print(Person)
#对对象的属性进行修改或者增加、删除
person.age = 18
person.height = 170
person.name = 'lisi'
print(person.height)
del person.age  #不能用del删除类属性，因为对象本身没有存gender，删除时尝试删除对象自身属性
#没有给person的gender属性定义故报错
print(person.age,)  #只删除了person这个对象里面的age，但是保留了类person里的age
#对方法的添加或修改
def drink(self):
    print("喝饮料")
#需要导入一个库，将新定义的函数与对象绑定起来
from types import MethodType
person.drink =  MethodType(drink,person)  #方法不要加括号，加了括号等于说将其调用，MethodType参数前面为方法，后面为要绑定的对象
person.drink()
person1 = Person()
person1.drink()  #对象之间的属性和行为是不共享的
#方法的添加
def say(self):
    print("说话")
person.speak = MethodType(say,person)
person.speak()
del person.speak #不要带括号

#构造函数及析构函数
class Person1:
    def __init__(self,name,age):  #记住构造函数是双下划线
        self.name = name  #绑定到了每个具体的对象中
        self.age = age
        print("我是构造函数，我被调用了")
    def say(self):
        print(f"{self.name}在说话")
    def __del__(self):  #不推荐用的原因之一就是，如果下面还有类的定义和调用，那么这个析构函数会在程序最后面一个类结束时调用，即对象被销毁的时候才调用
        print("我是析构函数，我被调用了")

person2 = Person1('wangwu',25)
person2.say()

#类属性和方法的类别
#1.类属性：在定义时所定义的属性，不与self绑定
#如果类的所有的实例需要使用同一个数据时，就可以将该变量设为类属性
class Circle:
    PI = 3.1415926
    def __init__(self,radius):
        self.radius = radius  #注意Circle.radius和self.radius差别很大，前一种是修改类属性，而后面一种是修改对象本身的属性，后面的方法不会影响其他对象以及类本身
    def area(self):
        print(f"圆的面积是{self.PI*self.radius*self.radius}")
circle = Circle(5)
circle.area()

class BankCount():
    total_amount=0
    def __init__(self,name,init_money):
        self.total_amount+=init_money
    def save_money(self,amount):
        self.total_amount+=amount
    def expend_money(self,amount):
        self.total_amount-=amount
my_bank=BankCount("zhangsan",1000)
my_bank.save_money(5000)
print(my_bank.total_amount)
#2.实例属性
#__dict__:用来查看对象的属性，只能查看和self绑定了的属性
print(person.__dict__)  #查看对象属性
print(Person.__dict__)  #查看类属性
#3.实例方法：类中的函数，第一个参数是self的就是实例方法，就是对象调用的方法
#4.静态方法：有自己的参数，和类里的数据据不共享，类和对象都可以调用
#静态方法上面有一个标志：@staticmethod
class Calculator:
    @staticmethod
    def add(a,b):
        print(a+b)
Calculator.add(1,3)
jisuanqi = Calculator()  #类调用静态方法
jisuanqi.add(2,4)  #对象调用静态方法
#5.类方法：属于类本身的方法，用来访问和修改类属性，不能访问实例属性
class Animals:
    name= 'Dog'
    @classmethod  #类方法标识符
    def change_name(cls,name):  #cls传入的是类本身的地址,实际上cls和Animals都同为类Animals
        cls.name = name
        print(cls)
print(Animals)
animals=Animals()
animals.change_name("cat")

