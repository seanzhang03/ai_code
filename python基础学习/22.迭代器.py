#迭代器是一个实现了迭代器协议的对象，需要同时具有__iter__()和__next__()方法
#__iter()__方法用来创建迭代器本身，返回本身，使其能够用在for循环及其他需要迭代器的地方
#__next()__方法每次迭代调用，返回序列中下一个元素，迭代完成抛出StopIteration类型的异常
#可迭代对象是实现了__iter()__方法的对象，但不一定有__next__方法
#所有的迭代器都是可迭代对象，但不是所有的可迭代对象是迭代器

#创建一个列表，这是一个内置的可迭代对象
my_list = [1,2,3,4,5]
#使用iter()函数来获取列表的迭代器
list_iterator = my_list.__iter__()
print(list_iterator)
print(type(list_iterator))
print(list_iterator.__next__())
print(list_iterator.__next__())
print(list_iterator.__next__())

#使用迭代器的__next__()方法来遍历列表
try:
    while True:
        #获取下一个元素
        item = list_iterator.__next__()
        print(item)
except StopIteration:
#没有更多元素时，迭代器抛出StopIteration异常
    print("Iteration id complete.")

#使用迭代器的__next__()方法来遍历字典
my_dict = {1:'one',2:'two',3:'three'}
dict_iter = my_dict.__iter__()  #迭代的是key值
print(type(dict_iter))
try:
    while True:
        item = dict_iter.__next__()
        print(item)
except StopIteration:
#没有更多元素时，迭代器抛出StopIteration异常
    print("Iteration id complete.")

#自己编写一个range迭代器
class MyRangeIterator:
    def __init__(self,end):
        self.end = end  #设置迭代器的结束值
        self.num = 0  #设置当前迭代的数值，初始为0
    def __iter__(self): #实现__iter__方法，返回迭代器本身
        return self  #因为迭代器就是实例本身，所以返回self
    def __next__(self):  #实现__next__方法，返回下一个值
        if self.num<self.end:  #如果当前数值小于结束值
            value=self.num  #获取当前数值作为要返回的值
            self.num+=1  #当前数值+1，为下次迭代做准备
            return value  #返回当前数值
        else:
            raise StopIteration  #抛出异常，结束迭代

for i in MyRangeIterator(5):
    print(i)

#迭代器的访问只能从前往后按顺序访问，只能按照一种规则往下走
mylist_iterator = my_list.__iter__()
for i in mylist_iterator:
    print(i)
#迭代器是一次性的，访问完后就失效
for i in mylist_iterator:
    print(i)