#python的并发是伪并发
#线程是os能够进行运算调度的最小单位，被包含在进程中，是进程内的实际执行单元，进程是资源分配的最小单位，线程是调度的最小单位
#与进程创建不同，线程在创建时除了会申请线程本身所必须的资源之外，其他的资源如内存空间、文件描述符等资源会使用进程已存在的资源，
# 一个进程中的多个线程会共享本进程的内存空间、文字描述等大部分资源。要注意，线程不具备进程级别的隔离性，一旦进程崩溃，虽不影响其他进程，但该进程内所有线程都终止
#多线程：线程是os进行运算调度的最小单位，被包含在进程之中，是进程的实际运作单位，线程共享进程内存空间，os可在同一进程空间中迅速切换不同线程，实现并发

#全局变量锁(GIL)：
#多线程：CPython解释器有一个全局解释器锁(GIL)，确保同一时刻只有一个线程执行Python字节码，因此即使是多核CPU，用多线程的python程序也无法实现真正并行计算，GIL限制线程在执行cpu密集任务的效率
#多进程：每个python有自己的python解释器和内存空间，因此GIL不限制多进程，多进程可以绕过GIL，充分利用多核cpu进行并行计算

#python中，多线程通过threading模块实现，该模块允许程序员创建、启动、同步多个线程，提供一系列API来支持线程间同步和通信
#通过threading模块的Thread类来创建进程
#threading.Thread(group=None,target=None,name=None,args=(),kwargs=None,*,daemon=None)
#group: 应该始终为 None，保留供未来扩展使用。
#target: 是一个可调用的对象（函数），该线程启动时，这个对象将被调用。如果不提供，则不会运行任何东西。
#name: 线程名称。默认情况下，将分配一个唯一的名称。
#args: 传递给 target 函数的位置参数，默认是一个元组。
#kwargs: 传递给 target 函数的关键字参数，默认是一个字典。
#daemon: 指定线程是否为守护线程。如果设置为 True，则该线程会在主线程结束时自动退出。如果是 None，则继承自创建它的线程。

import threading
import time
from threading import Thread
def func():
    print("hello")

t1 = threading.Thread(target=func,)
t1.start()
func()
t1.join()
#start(): 启动线程活动。使用start去启动线程，会调用run()方法，它会创建一个新的线程来执行run()方法中的代码。
#run(): 表示线程活动的方法。可以在子类中重写此方法，重写之后执行重写的代码。通常不需要直接调用run方法，应该调用start方法去启动线程，如果直接调用run方法(没有通过start方法去启动线程)那么run方法中的代码将在当前线程中同步执行，而不是在新的线程中执行。
#join(timeout=None): 等待线程终止。timeout参数是可选的，表示等待的最长时间（以秒为单位）。如果没有指定timeout，则该方法将无限期等待。
#is_alive(): 返回线程是否还活着。
#getName(): 返回线程名。
#setName(name): 设置线程名。
#isDaemon(): 返回线程的守护状态。
#setDaemon(daemon): 设置线程的守护状态。必须在start开始前设置。
#name: 线程名称。
#ident: 线程的标识符。如果线程尚未启动，则为None。(类似于PID)
#daemon: 线程的守护状态。

def func1():
    print("hello")

if __name__ == "__main__":
    t2 = threading.Thread(target=func,)
    t2.start()
    print(t2.is_alive())  #func1中没有时延的话，不能保证t2的存活状态
    t2.join()
    print(t2.is_alive())

def func2():
    print("Function 2 is running.")
    time.sleep(2)
    print("Function 2 has finished.")

def func3():
    print("Function 3 is running.")
    time.sleep(2)
    print("Function 3 has finished")

if __name__ == "__main__":
    start_time = time.time()
    process = Thread(target=func3)
    process.start()
    #在主程序允许func2
    func2()
    process.join()
    total_time = time.time() - start_time
    print(f"Total eecution time:{total_time:.2f}seconds")
#假设子线程func3先抢到锁，先执行第一个输出语句，然后遇到sleep进行休眠并释放锁，然后主线程func2抢到锁，也打印第一个输出语句。然后主线程遇到sleep也释放GIL锁
#然后这两个进程就相互抢锁释放锁直到休眠完成

