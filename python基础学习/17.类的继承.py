#python中，一个类可以被继承，也可以去继承其他类，其中被继承的类称为父类或者基类，继承的类称为子类
#继承过程中，子类会继承父类所有属性和行为，一个子类可以有多个父类， 一个父类可以有多个子类  
#一般不推荐修改父类里的属性，因为修改父类会导致所有子类属性发生改变
#python3.x中，所有类有一个父类object，子类有object所有的属性和方法

#类的继承分类：
#单继承：一个类只有一个父类，即单继承。当子类中存在与父类相同的属性和方法时，子类的属性和方法会覆盖父类的属性和方法
#多继承：一个类有多个父类，即多继承。多继承可以提供更多的功能，但可能导致继承冲突，比如子类和多个父类有相同的属性和方法
#那么此时使用时该属性或方法，顺序为：子类>从左到右第一个父类>第二个>第三个
#复杂的继承关系用mro

#子类调用时优先调用自己所拥有的，没有该属性或方法时，才会去父类中找
class A:
    a=1
    b=2
    c=3
    def say(self):
        print("我是A")
    def question(self):
        print("你是谁？")

class B(A):
    a = 4 
    b = 5
    def say(self):
        print("我是B")
b = B()
print(b.a)
print(b.b) #子类找不到变量的值时，才会取父类中找
b.say()

#多继承
class C:
    a = 100
    def say(self):
        print("我是C")
    def run(self):
        print("我会跑步")

class D:
    a = 200
    def say(self):
        print("我是D")
    def swim(self):
        print("我会游泳")

class E(C,D):
    pass
e = E()
print(e.a)  #调用从左到右第一个父类中的属性a，即C中的属性a的值
e.run()
e.swim()
print(E.mro())  #[<class '__main__.E'>, <class '__main__.C'>, <class '__main__.D'>, <class 'object'>]

#继承类中方法的重写
class F:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def add(self):
        return self.x+self.y
    
class G(F):
    def __init__(self,x,y,z):
        F.__init__(self,x,y)
        self.z = z
    def add(self):
        print(F.add(self)+self.z)
g = G(1,2,3)
g.add()

#super()函数：根据mro继承顺序去搜索父类中的指定函数，并且自动绑定好self参数
#一行super()函数可以完成多行初始化方法及其他方法的实现
class A1:
    def __init__(self):
        print("A1")
class B1(A1):
    def __init__(self):
        super().__init__()
        print("B1")
class B2(A1):
    def __init__(self):
        super().__init__()
        print("B2")
class C1(B1,B2):
    def __init__(self):
        super().__init__()  #由于有两个父类本来该写2个父类的初始化方法，这里直接用一个super方法代替了
        print("C1")
c1 = C1()
