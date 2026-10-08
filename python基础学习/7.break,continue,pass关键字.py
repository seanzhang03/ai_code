# break,continue,pass
#pass占位符，用来占据目前还未构思出来的功能块

#输出一个数的所有因子
num = int(input("请输入一个整数"))
for i in range(1,num+1):
    if num % i == 0:
        print(f'{i}是{num}的一个因子')

a = -15
b = -15
print(id(a),id(b))
c = float('-inf')
print(c)
#无穷大 无穷小和NAN不是数字