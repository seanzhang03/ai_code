#元组与列表相似，不同在于元组元素不可修改 
#元组的查找
#len()
#max()
#min()
#in /not in
#del 删除元组

#序列：可以按照索引位置访问元素的有序数据结构，标准序列包括list、tuple
# 和str
#sorted()函数可以对序列进行排序，返回一个新的列表，原有序列不变
#reversed()函数可以将序列反转，返回一个新的迭代器，原有序列不变
#all()函数可以判断序列中的所有元素是否都为True，返回值为布尔值
#any()函数可以判断序列中的至少有一个元素为True，返回值为布尔值

#enumerate()函数将一个可遍历的数据对象的下标和元素组合起来，函数返回枚举对象，
#是包含元组的序列，通过强转和for循环进行查看
#eg.:(0, 'a')
#zip()将多个可迭代对象中对应位置的元素打包成一个元组，返回由这些元组组成的迭代器
#同时处理多个序列时有用，同样需要强转和for循环查看

#元组推导式的应用是用圆括号

#default参数，来指定空序列的提示词
empty_list = []
print(min(empty_list,default="此序列为空序列"))
#sum()函数
num_list = [1,2,3,4,5]
print(sum(num_list))
#reversed()函数,不会影响原有数据
tuple1 = (1,2,3,4,5)
tuple1=tuple(reversed(tuple1))
print(tuple1)
#sorted()函数,不会影响原有数据
tuple1 = (1,2,3,4)
tuple1=tuple(sorted(tuple1,reverse=True))  #True为升序，False为降序
print(tuple1)
#enumerate()函数
tuple2 = ('a','b','c')
for i in enumerate(tuple2,start=1): #第一个下标值可以通过start修改
    print(i)
#zip函数
tuple3 =(5 ,6 ,7 ,8)
print(list(zip(tuple1,tuple3))) #
print(list(zip(tuple2,tuple3))) #以数据少的元组作为基准
#map()函数
tuple4 = ("banana" ,"apple", "peach",  "orange")
temp = map(sorted,tuple4) #map中前面填要引入的函数，注意不要加括号，后面填入要处理的数据对象
#map会将其中的函数作用于可迭代对象的每个元素上，即将banana的每个字符拆开进行排序
print(list(temp))
#filter()函数.将序列中的元素传入到参数函数中，并将结果 为True的值返回，返回值要通过强转或for循环查看
tuple5 = ('123','5d1fc','abcd')
t1 = filter(str.isdigit,tuple5)
print(list(t1))