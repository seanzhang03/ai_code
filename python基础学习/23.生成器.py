#生成器是一种特殊的迭代器，可以在需要时动态生成值，避免一次生成所有值所占用的大量内存
#python中，生成器可以通过函数定义和生成器表达式来创建
#惰性求值：生成器不在创建时生成所有值，而是逐个生成值，意味着生成器可以在需要时再去生成
#使用yield关键字：只有yield被调用时，生成器才返回一个值，并且程序暂停执行，直到下一次迭代才继续执行
#普通函数用return返回值但生成器函数用yield关键字返回值
#生成器可处理大型数据集而不占用太多内存，只有需要时才生成值
#状态保持：生成器函数在每次产生一个值后暂停执行，保持当前状态，包括局部变量的状态和当前执行位置，再次调用生成器时，从上次yield语句后地方继续执行

#生成器函数：在调用时，不会立即执行函数里面的代码，而是会先返回一个生成器的对象，当调用生成器对象的__next__()方法时
#才会进入函数中并执行函数里面的代码，遇到yield关键字后，函数的执行将会暂停，并将yield后面的表达式作为当前迭代的值返回
#然后每次调用生成器的__next__()方法或使用for循环进行迭代时，函数会从上次暂停的地方继续执行，直到再次遇到yield关键字
#并再次返回一个值，直到无法继续生成为止
#定义生成器函数
def count_up_to(max):
    count=1
    while count <=max:
        yield count
        count+=1

res = count_up_to(5)
print(res)
for num in res:  #生成器也是一次性的，调用完了就失效
    print(num)

#应用到斐波拉契数列
import time
def fibonacci():
    a,b = 0,1
    while True:
        yield a
        a,b = b,a+b
fib = fibonacci()
count = 1
for i in fib:
    print(f"第{count}个数是",next(fib))
    count+=1
    time.sleep(5)