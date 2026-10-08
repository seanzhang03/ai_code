#函数是具有独立功能的代码块，使用函数名来封装，通过函数名调用
#出现目的就是为了代码的复用
#函数代码块以def关键词开头，后面接函数名和圆括号()及一个冒号，表示函数的开始
#传入的参数在圆括号内进行定义，冒号后另起一行，并缩进
#用return结束函数，选择返回一个值给调用方，没有return的返回None
def add(x,y): 
    z=x+y
    return z
print(add(1,5)) #传参除了可以直接使用数据外还可以传变量的值
#参数是函数定义时圆括号内的变量，来接受调用函数时外部传递进来的数据
#其最大作用是让函数在不同情况下重复使用
#形参时定义函数时的参数变量，实参是实际调用时的参数变量
#函数的返回值可以是一个或者多个值，多个值则默认为元组类型
#局部变量、全局变量，作用域不同，局部变量作用于函数内部，而全局变量作用于整个程序
#在函数内部用global定义变量可以使其变为全局变量 

#闭包函数
def nth_power(exponent):
    def exponent_of(base):
        return base ** exponent
    return exponent_of
square= nth_power(2)
cube = nth_power(3)
print(square(2))
print(cube(3))

#匿名函数lambda：无名字的函数，只在函数体只有依据和返回值只有一个时使用
#语法格式 lambda 参数列表:表达式 该函数自带return，要有一个值来接收
#可用任意数量参数但是只能有一个表达式，生命周期短，调用后立即回收
#匿名函数可用可变参数或者默认参数
lambda x,y:x+y
print

#内置函数
#abs 取绝对值
x=-3.14
print(abs(x))
#round函数返回四舍五入的值，参数为要操作的对象和保留小数位数
pi=3.1415923
print(round(pi,4))
#help函数，查看函数的原型和说明文档
#内置函数一般都有说明文档，自定义函数需要用户填写
#help(round) #其参数是函数名，不要带括号
def test():
    '''
    这是一个测试函数的说明
    '''
    print('测试函数')
help(test)

#函数只有在调用的时候才会执行
#函数在定义的时候，python解释器只会检查语法，不会主动执行函数   
#pass:在函数刚开始定义没有写功能时作为占位符防止解释器报错

#位置参数：参数传递时实参的顺序和个数必须和形参一致
def sub(x,y):
    print(x-y)

#关键字参数：使用形参名字=实参的方式传递，不考虑形参的位置
#个数需要保持一致
#调用函数时，第一个传入的参数是关键词传参时，那后面的参数就不能用位置传参了
sub(y=2,x=1)

#默认参数，默认参数定义时必须放在形参的最右边
def add1(x,y,z=1):  #默认z=1
    print("x的值为",x)
    print("y的值为",y)
    print("z的值为",z)
add1(1,2)  #可以只写两个实参，z的值自动默认为1
#默认参数在调用函数时如果不需要修改默认参数的值就可以不传递
#如果需要修改默认参数的值，可以传递实参来覆盖掉默认参数的默认值
#默认参数可以配合关键字参数来使用
add1(z=3,x=1,y=2)

#位置不定长参数：在函数定义时，使用*args来表示，打包成一个元组
#如print()函数
def myfunc(*args):
    print(len(args))
    print(type(args))
    print(args)
myfunc(1,2,3,4,'asd','zxc')
#之所以打包成元组是因为元组有特性打包和解包，打包就是将多个值打包成一个元组
#打包的用法
def test():
    return 1,2,3,4
ret = test()
#解包：将一个元组的元素拆开分别赋值给对应的变量
a,b,c,d = test()
#不定长位置参数在定义时，如果右边还有其他的参数，必须要使用关键字参数传参
def myfunc2(*args,x,y):
    print(args)
    print(x)
    print(y)
#myfunc2(1,2,3,4,5) #这样输出会报错，要用关键字传参
myfunc2(1,2,3,x=2,y=3)

#关键字不定长参数：允许接受任意数量的关键字参数，在函数定义中以**kwargs表示
#传入的关键字参数会被打包成一个字典传递给**kwargs
def func(** kwargs):
    print(kwargs)
    print(type(kwargs))
func(x=1,y=2,z=3)
def mul(**kwargs):
    result = 1
    for key in kwargs.keys():
        result = kwargs[key] * result
    print(result)
mul(x=1,y=2,z=3)

#位置参数、不定长位置参数以及不定长关键字参数混合使用
def mix(x,*args,**kwargs): #这里要将args放在定长的形参后面，若放到前面会导致定长形参无法传值
    print(x)
    print(args)
    print(kwargs)
mix(1,2,3,z=4,y=5) 
#元组的解包
def test2(x,y,m,n):
    print(x,y,m,n)
my_tuple=(1,2,3,4) 
#test2(my_tuple)  #会报错，因为将args整个元组的值传给了x
test2(*my_tuple)  #正确方式是加*给这个元组解包，将元组里面含有的每个元素传给形参
#字典的解包
my_dict = {'a':1,'b':2,'c':3,'d':4}
my_dict2 = {'x':1,'y':2,'m':3,'n':4}
#test2(**my_dict) #字典解包的时候，实参中的key值要与函数形参中的变量名保持一致
test2(**my_dict2)
test2 (**{'y':2,'m':1,'n':3,'x':4}) #顺序不一致也可以，但是要每个key能对应上每一个形参变量名

#函数的返回值
def calculate(x,y):
    z1=x+y
    z2=x-y
    z3=x*y
    z4=x/y
    return z1,z2,z3,z4  #python中函数的返回值可以是多个
z1,z2,z3,z4=calculate(3,4)
my_tuple2 = calculate(3,4)
print(z1,z2,z3,z4,my_tuple2)

#函数内部是可以访问全局变量的，但是函数外部不可以访问到函数内部的局部变量
#函数内部存在变量与函数外部的变量名字相同时，局部变量会覆盖掉全局变量
num = 1
def myfunc3():
    num=2
    print(num)
myfunc3()
#使用global将局部变量转换为全局变量
num=1
def myfunc4():
    global num
    num=3
    print(num) #将局部变量赋值后，函数内外输出结果都保持一致了
myfunc4()
print(num)
num2 = 5
def myfunc5():  #因为改成了全局变量，所以修改前函数内外id号一致，修改后函数内外id号一致
    global num2
    print("函数内修改前的id号",id(num2))
    num2=10
    print("函数内修改后的id号",id(num2))
print("函数外修改前的id号",id(num2))
myfunc5()
print("函数外修改后的id号",id(num2))
#定义函数时候，不要让函数名和内置函数名一样，否则自己写的会覆盖掉解释器内部的函数

#嵌套函数
#内部函数除了在外部函数中调用之外，是无法访问到的
#嵌套函数的作用域：内部函数的局部变量是可以覆盖外部函数的局部变量的
#内函数中：内函数的局部变量>外函数的局部变量>全局变量
def outer_func():
    x=1
    def inner_func():   
        #使用nonlocal关键字，可以在内函数中修改外函数的变量值   
        #global修改的是局部变量，nonlocal修改的是上一层嵌套的函数的变量
        #global和nonlocal不能对同一变量生效
        #nonlocal x
        x=2
        print("这是内部函数x的值",x)
    inner_func()   #在外函数中调用内函数，才可以访问到
    print("这是外部函数x的值",x)
    return inner_func  #以内函数作为返回值进行返回，不用带圆括号
ret = outer_func()  #相当于起了个别名
print(ret)
ret()
#嵌套函数的特性：当内部函数访问外部函数的某个变量时
#该变量不会随着外部函数的调用完毕而销毁，而是被内部函数所保留
def outer_func1():
    x=1
    def inner_func1():
        print(x)
        return inner_func1
ret=outer_func1
ret()
#手写一个pow函数，用嵌套函数完成
def outer_func2(exp):
    def inner_func2(base):
        return base ** exp
    return inner_func2
ret = outer_func2(2)
result = ret(3)
print(result)

#lambda 表达式
res = lambda x,y:x+y
print(res(1,2))