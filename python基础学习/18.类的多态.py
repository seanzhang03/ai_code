#多态：不同对象对同一方法做出的不同相应，用于设计更加灵活的代码
str1="sadassffa"
my_list=[1,2,3,4,5]
my_tuple=(1,2,3,4)
print(len(str1)," ",len(my_list)," ",len(my_tuple))

class Cat:
    def say(self):
        print("miao~~~~")
class Dog:
    def say(self):
        print("wang~~~~")
class Sheep:
    def say(self):
        print("mie~~~~")
def call(x):
    x.say()
cat = Cat()
dog = Dog()
sheep = Sheep()
call(cat)
call(dog)
call(sheep)