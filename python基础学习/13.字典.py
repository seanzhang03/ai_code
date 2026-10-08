#字典是无序的数据类型，字典的数据是按照键值对的方式来存储，键值对可修改
#键是唯一的，且键和值一一对应，若定义了相同的键，则新定义的值会覆盖原值
#键必须不可变，可以用数字、字符串或者元组等不可变数据类型，但是不能用列表
#值可以是任何数据类型
#字典的访问，只能通过唯一的键来访问对应的值，若访问不存在的键则会报错

#键值对的修改
my_dict = {'key1' : 'value1' , 'key2' : 'value2' , 'key3' : 'value3'}
#修改单个键值对
my_dict['key1'] = '1'
print(my_dict)
#修改多个键值对，用update(),用来修改多个键值对
my_dict.update({'key1': 2 ,'key3' :3})
print(my_dict) 
#还可以通过直接赋值来实现，若赋值没有该键值对，则会添加这一对新键值对
my_dict["city"] = "London"
print(my_dict)

#键值对查找
#直接通过key值来查找
print(my_dict['key2'])
#用get函数来查找，get函数查找时，前面一个参数是key值，后面可以跟一个数据类型，来返回这个数据值
print(my_dict.get('key3','你要查找的键值对不存在'))
print(my_dict.get('key4','你要查找的键值对不存在')) #可以指定键值对不存在时的提示词，若不指定则返回None
#setdefault()函数，若原集合能查找所指定的键值对时返回其key值，否则在原集合基础上增加一个新的键值对并返回所创建的key值
print(my_dict.setdefault('key2','nihao'))
print(my_dict.setdefault('key4','nihao'))
print(my_dict)

#键值对的删除
my_dict2={'key1':1,'key2':2,'key3':3,'key4':4}
#pop()函数，返回的是被删除的值，可以指定键值对的key值来实现删除
temp= my_dict2.pop('key2') #返回值为key值对应的value值
print(my_dict2," ",temp)
#字典中没有remove方法，remove方法是针对列表的
#del函数，删除成功后没有返回值，和pop函数一样可以给定要删除键值对的key值
del my_dict2['key4']
print(my_dict2)


#键值对的其他操作
#len函数获取键值对的个数
print(len(my_dict))
#copy函数，对字典进行浅拷贝
my_dict1 = my_dict.copy()
print(my_dict1)
#keys函数，返回字典中所有键值对的key值
print(my_dict.keys(),'对应的数据类型是',type(my_dict.keys())) #keys返回的数据类型是字典的key值
#values函数，返回字典中所有键值对的value值
print(my_dict.values(),'对应的数据类型是',type(my_dict.values())) #values返回的数据类型是字典的value值
#items函数，返回字典中所有的键值对
print(my_dict.items())

#字典推导式
square_dict = {y : y**2 for y in range(1,6) }
print(square_dict)