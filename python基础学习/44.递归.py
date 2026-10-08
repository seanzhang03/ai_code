#递归（Recursion），是一种解决问题的方法，其精髓在于将问题分解为规模更小的相同问题。持续分解，直到问题规模小到可以用非常简单直接的方式来解决。
#递归的问题分解方式非常独特，其算法方面的明显特征就是：在算法流程中调用自身。
#递归为我们提供了一种对复杂问题的优雅解决方案，精妙的递归算法常会出奇简单，令人赞叹。
#递归三定律：
#递归算法必须有一个基本结束条件（最小规模问题的直接解决）
#递归算法必须能改变状态向基本结束条件演进（减小问题规模）
#递归算法必须调用自身（解决减小了规模的相同问题）
def fib(n):
    fib_list= []
    a,b=0,1
    while len(fib_list) < n:
        fib_list.append(a)
        a,b = b,a+b
    return fib_list
print(f"{fib(10)}")

def fibonacci(n):
    if n<= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0,1]
    else :
        fibonacci_list = fibonacci(n-1)
        fibonacci_list.append(fibonacci_list[-1] + fibonacci_list[-2])
        return fibonacci_list 

print(f"{fibonacci(10)}")