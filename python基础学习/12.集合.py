#集合是无序的不重复元素序列，有可变和不可变集合，定义时的序列和访问的序列顺序不一定相同
#集合元素不可重复
#集合元素定义后不可以修改，意味着集合的元素只能是数字、字符串和元组
#因为这几个数据类型是不可以修改的，即其中的元素一定是不可变元素.
#集合作为去重的容器
#可变集合的添加（集合里面已有的元素不能修改，但是可以增加元素的个数）
#不可变集合，不仅集合元素不可变，集合元素的个数也不可变

#可变集合的定义
myset = {1,2,3,4 ,'ab','c',1,3,(1,2,3)}
print(myset)
#add()函数，向可变集合中添加单个元素
myset.add(5)
print(myset)
#update()函数，向可变集合中添加多个元素
#并且将序列中的元素拆分成单个元素添加到可变集合中
myset.update([15],('a','b','c')) #要将15改为可迭代对象
print(myset)

#可变集合元素的删除
myset={1,2,3,4,5}
#remove()函数，删除指定元素，若不存在则报错
myset.remove(5)
print(myset)
#discard()函数，删除指定元素，若不存在则不报错
myset.discard(0)
print(myset)
#pop()函数，删除并返回可变集合中的第一个元素，若集合为空则报错
temp = myset.pop() #与list不同，set的pop函数是随机删除，而set是删除最后一个，且set的pop函数无法指定删除的元素
print(myset,'删除元素为',temp)

#可变集合元素的查找
if 2 in myset:
    print("2在集合中")

#其他操作
#len()函数，集合也能通过len来获取
#set()函数  该函数创建的是可变集合
set1 = set()
print(set1,' ',type(set1)) #不给set函数赋参数值，则会创建一个空集合
#set1 = set(1)  #set后面的参数必须是一个序列，即可迭代对象
print(set1)
set1=set([1,2,3])
print(set1)
#clear()函数：清空集合，让集合变成一个空集合
set1.clear()
print(set1)
#intersection()函数：求两个集合的交集
set2= {2,3,4}
set3={4,5,6}
print(set2.intersection(set3))
#union()函数：求两个集合的并集
print(set2.union(set3))
#issubset()函数：判断一个集合是否是另一个集合的子集
set4={2}
print(set4.issubset(set2))
#issuperset()函数：判断一个集合是否是另一个集合的父集
print(set2.issuperset(set4))
#不可变集合的创建，使用frozenset()函数创建
#需要填入一个为序列的参数
set5 = frozenset((1,2,3,4))
print(set5)