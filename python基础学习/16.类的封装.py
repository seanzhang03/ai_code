#类的封装：将数据和方法封装到一个类中，通过设置访问权限可将类的属性和方法隐藏在类的内部，
#防止类的属性和方法被外部直接访问和修改，提高代码的安全性和可维护性
#给属性名和方法增加下划线设置权限，根据下划线个数分为不同类型：
#1.单下划线前缀：单下划线开头命名的属性和方法，表示该属性或方法是内部使用的，但是是人为规定的，实际程序是可以访问的
#2.双下划线前缀：真正的设置私有权限的方法，通过在属性名或行为名之前添加双下划线就可以将属性或行为定义为私有的且不可被对象访问
#比如在类里面用双下划线前缀，实例化出来的对象是无法找到被隐藏的属性
#3.双下划线前后缀：python中特殊的属性或方法，是python内置好的内容，有特殊的定义和内容，不推荐自己定义

#私有属性的设置：在属性和方法名前添加双下划线前缀
class Person:
    def __init__(self,name,password):
        self.name= name
        self.phone_number="123****"
        self.__password=password  #用双下划线前缀来隐藏该属性
    def say_passwword(self):
        print(f"银行卡密码是{self.__password}")  #可以在类中进行该属性的访问
p1 = Person("zhangsan","123456")
print(p1.name)
#print(p1.__password) 访问不到
p1.say_passwword()

#利用私有属性来阻止直接的访问修改
class BankCount:
    def __init__(self,name,password):
        self.name = name 
        self.__password = password
        print(self.__password)
    def change_password(self,new_password):
        self.__password = new_password
        print(self.__password)
myCount = BankCount("zhangsan","123456")
myCount.change_password("654321")