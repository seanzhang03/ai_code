#list：有序的元素集合，来存储一组有序的数据，可以包含任意数量元素，且每个元素
#可以是不同的数据类型，和字符串不同的地方在于，list中的元素可修改。
#list的访问也是通过下表和切片访问
#list的加法和乘法跟字符串的加法和乘法是一致的
print([1,2,3]+[4,5,6])
print([1,2,3]*3)
#浅拷贝：新对象与原对象内容一致，但是内部的可变元素只是原来的引用，而非独立对象
#数字，字符串这些不可变元素在浅拷贝后修改新对象不会导致远对象中的变量发生改变
#深拷贝：创建的新对象，该对象和其中的所有元素都是完全独立的新对象，都是一个新的
#副本，而非引用

#列表元素的增加
list = [1,2,3,4,5,6]
#append()函数将一个元素添加到列表的末尾
list.append(7)
print(list)
#insert()函数将一个元素插入到指定的位置,第一个参数是位置，第二个是要添加进去的参数
list.insert(7,8)
print(list)
#extend()函数将一个列表中的元素添加到当前列表的末尾
list.extend([9,10])
print(list)

#列表元素的删除
list2 = [1,2,3,4,5,6,7,8,9,10]
#remove()函数删除指定的元素，返回删除的元素None
print(list2.remove(7))
print(list2)
#pop()函数删除指定位置的元素，返回删除的元素
print(list2.pop(0)) #若不指定位置，则弹出最后一个元素
print(list2)
#clear()函数清空列表，返回None
#list2.clear()
#print(list2)
#del指定下标时删除对应的元素，不指定删除整个列表对象，会导致整个list下面代码
#无法使用
list3 = [1,2,3,4,5,6,7,8,9,10]
del list3[0]
# print(list3) 由于删除后访问会导致报错

#列表元素的修改
list3 = [1,2,3,4,5,6,7,8,9,10]
#下标修改
list3[0] = 0
print(list3)
#切片修改
list3[0:3]=[0,0,0] # 赋值的数量和修改的元素数量要一致
print(list3) 

#列表元素的查找只有index()方法，没有find()方法

#其他操作
#reverse()函数将列表中的元素反转，返回None，不需要参数直接调用
print(list3)
#sort()函数，列表的排序操作
list4 = [5,4,8,6,1,3,2]
list4.sort(reverse=True) #True表示降序排序，False表示升序排序
print(list4)
list5 = ['abc','defg','hi']
list5.sort(reverse=True,key=len) #按照字符串长度来进行排序
print(list5)

#列表的浅拷贝
list6 = list4.copy()
print(list6)
#深拷贝
import copy
list7 = copy.deepcopy(list4)
print(list4 is list7) #深拷贝两者指向不一样
print(list7)
print("地址分别是",id(list4),"和",id(list7))

#列表推导式的应用
#用for循环
list8 = [1,2,3,4,5,6]
list9 = [0,0,0,0,0,0]
for i in range(len(list8)):
    list9[i] = list8[i] ** 2
print(list9)
#列表推导式
squared_list = [x ** 2 for x in list8]
print(squared_list)
#使用条件控制语句来控制赋值
list10 = [x **2 for x in list8 if x<=4]
print(list10)

#多层列表嵌套的遍历
list11 = [[1,2,3],[4,5,6],[7,8,9]]
new_list = []
for i in range(len(list11)):
    for j in range(len(list11[i])):
        print(list11[i][j],end=" ")
        new_list.append(list11[i][j])
print(new_list)
#使用for循环
#列表推导式
list12 = [y for x in list11 for y in x ] #in后面跟的变量要先定义出来再用
                                         #所以要先把for x放前面定义x
print(list12)
