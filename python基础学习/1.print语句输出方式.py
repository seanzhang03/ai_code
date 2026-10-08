name = 'Sean Zhang'
age = 23
print("My name is {} and my age is {}" .format(name , age))
#使用 %进行占位
print("%s %d" %(name,age))
print("%d" %5)
# format 和占位符都有位数限制
# m.n m指定位数，n指定精度，即小数位数
weight = 78.123456789
print("My name is {} and my weight is {:.2f}" .format(name , weight))
# f-string方法 使用{}占位，并且直接插入表达式
print(f"My name is {name} and my wweight is {weight}")
#input 函数 变量=input("提示词")，input获取的数据都会转换为字符串