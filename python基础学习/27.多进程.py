#python中，multiprocessing库提供了创建和管理进程的方法，允许程序员创建进程，并提供一系列API来实现数据共享和通信
#使用方法：multiprocessing.Process(group=None,target=None,name=None,args=(),kwargs={},*,daemon=None)
#group：通常不使用，为可能扩展预留
#target：表示调用对象，即子进程要执行的任务，通常为一个函数名字
#name：进程名，默认情况下为Process-N，其中N是进程序号（非PID），可以通过这个参数来指定一个自定义名称
#args：调用target函数时传递的参数元组
#kwargs：调用target函数时传递的参数字典
#daemon：若设置为True则子进程是守护进程。当主进程结束时，所有守护进程都将被终止。默认为None，表示继承当前进程的守护进程设置

#进程状态
#守护进程：通常在系统启动时自动启动，并在后台执行特定的系统级任务，无需用户直接干预
#僵尸进程：已经结束但仍然存在于进程表中，等待父进程收集其退出状态的进程，不再占用系统资源，除了进程表中的一个条目，以及一个退出状态码
#孤儿进程：父进程已经结束，但他们仍在运行的进程，由于其父进程已经终止，他们会被init进程(PID为1)所领养，init负责处理这些孤儿进程，确保他们能够正常结束

from multiprocessing import Process,current_process
import os
import time
'''
if __name__ == '__main__':
    p1 = Process()
    p1.start
'''
'''
def say():
    print("in p1")
    print("Hello")
    print(os.getpid())

if __name__ == "__main__":
    print("in main")
    p1 = Process(target=say)
    print("make p1")
    p1.start()  #是多核，这里启动不会影响到主进程的执行，打印的同时子进程的两句话也会执行
    print('start')
    print(p1.name)
    print(p1.pid)  #也可以用os.getpid()来完成获取当前进程pid
    print(current_process().pid)
    print(os.getpid())
    p1.join()  #等待子进程完成 process、start、join三个步骤配套使用，缺一不可
    print("OK")
'''

'''
def say_hello(name):
    time.sleep(2)
    print(f"Hello {name},Nice to meet you!")

if __name__  == "__main__":
    start = time.time()
    process1 = Process(target=say_hello,args=('Alice',))  #多个args一定要用括号，并且每个arg之间要用逗号隔开，将Alice赋给了say_hello里面的形参
    process1.start()
    say_hello("Bob")  #通过并发执行比串行执行节约时间
    process1.join()
    exe_time=time.time()-start  #是2s而非4s，说明是同时进行的，因为如果是串行执行则一定大于4s
    print(exe_time)
'''

#进程间资源不共享
money = 100
def expend(money):  #开辟了一块独立的空间
    money-=20
    print("子进程",money)

if __name__ == "__main__":
    process1 = Process(target=expend, args=(money,))
    process1.start()
    process1.join()
    print("主进程",money)
