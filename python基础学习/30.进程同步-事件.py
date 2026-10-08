#事件：简单的同步机制，允许一个进程通知一个或多个等待的进程某些事件已经发生，也就是发送一个信号，而其他进程可以根据这个信号做出反应
#应用场景：一个进程等待另一个进程完成某项任务、控制多个进程间的简单通信、是按对共享资源的访问控制
#时间的基本方法
#is_set()：返回时间是否已设置的状态，如果被设置则返回True否则返回False
#set()：将事件设置为真状态，即True，表示可以唤醒正在等待该事件的所有线程或进程
#clear()：将事件设置为假状态，即False，表示没有进程被唤醒
#wait([timeout])：阻塞当前进程直到事件被设置为真状态或超时（若提供了timeout参数）。若没有设置，就会一直等待直到事件被设置
from multiprocessing import Event,Process
import time
'''
def producer(start_event,):
    start_event.set()  #设置事件告诉消费者可以开始消费
    while True:
        time.sleep(1)

def consumer1(start_event,):
    start_event.wait()  #等待进程被设置
    while True:
        print(1)

def consumer2(start_event,):
    start_event.wait()  #等待进程被设置
    while True:
        print(2)

def consumer3(start_event,):
    start_event.wait()  #等待进程被设置
    while True:  #子进程 在while中进入了死循环，不会被wait语句给阻塞，wait只能在刚开始去判断有没有唤醒
        print(3)

def consumer4(start_event,):
    start_event.wait()  #等待进程被设置
    while True:
        print(4)

def consumer5(start_event,):
    start_event.wait()  #等待进程被设置
    while True:
        print(5)

if __name__ =="__main__":
    start_event = Event()
    producer_process = Process(target=producer,args=(start_event,))
    producer_process.start()

    consumer1_process = Process(target=consumer1,args=(start_event,))
    consumer1_process.start()

    consumer2_process = Process(target=consumer2,args=(start_event,))
    consumer2_process.start()

    consumer3_process = Process(target=consumer3,args=(start_event,))
    consumer3_process.start()
    
    consumer4_process = Process(target=consumer4,args=(start_event,))
    consumer4_process.start()
    
    consumer5_process = Process(target=consumer5,args=(start_event,))
    consumer5_process.start()
    producer_process()
    consumer1_process.join()
    consumer2_process.join()
    consumer3_process.join()
    consumer4_process.join()
    consumer5_process.join()
    producer_process.join()
'''


    
from multiprocessing import Event,Process
import time

def producer(start_event,):
    #start_event.set()  #设置事件告诉消费者可以开始消费
    while True:
        start_event.set()
        time.sleep(2)
        start_event.clear()
        time.sleep(10)

def consumer1(start_event,):
      #等待进程被设置
    while True:
        start_event.wait()
        print(1)

def consumer2(start_event,):
      #等待进程被设置
    while True:
        start_event.wait()
        print(2)

def consumer3(start_event,):
      #等待进程被设置
    while True:  #子进程 在while中进入了死循环，不会被wait语句给阻塞，wait只能在刚开始去判断有没有唤醒
        start_event.wait()
        print(3)

def consumer4(start_event,):
     #等待进程被设置
    while True:
        start_event.wait()
        print(4)

def consumer5(start_event,):
      #等待进程被设置
    while True:
        start_event.wait()
        print(5)

if __name__ =="__main__":
    start_event = Event()
    producer_process = Process(target=producer,args=(start_event,))
    producer_process.start()

    consumer1_process = Process(target=consumer1,args=(start_event,))
    consumer1_process.start()

    consumer2_process = Process(target=consumer2,args=(start_event,))
    consumer2_process.start()

    consumer3_process = Process(target=consumer3,args=(start_event,))
    consumer3_process.start()
    
    consumer4_process = Process(target=consumer4,args=(start_event,))
    consumer4_process.start()
    
    consumer5_process = Process(target=consumer5,args=(start_event,))
    consumer5_process.start()
    producer_process()
    consumer1_process.join()
    consumer2_process.join()
    consumer3_process.join()
    consumer4_process.join()
    consumer5_process.join()
    producer_process.join()
    