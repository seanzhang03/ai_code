#条件变量是协调多个进程的一种机制，通常与锁一起使用来实现更复杂的同步模式，Condition对象可看作一个锁加一个或多个条件队列的组合
#multiprocessing.Condition(lock=None)来创建一个条件变量对象，其中lock可以替换为自己指定的Lock或RLock对象，若lock为None，自己创建一个新的RLock对象并使用
#acquire()：获取内部锁，若无法立即获得，调用者会阻塞到锁可用
#release()：释放内部锁
#wait()：释放内部锁，调用进程阻塞，直到接受通知，被唤醒时，会尝试获取锁。
from multiprocessing import Condition,Process
import time

def producer(condition):
    while True:
        condition.acquire()
        condition.notify_all()  #通知所有等待的消费者,notify(num)则是唤醒num个消费者
        condition.release()  #condition语句也可以使用with来代替acquire和release的过程
        time.sleep(3)  #模拟生产者的工作周期

def consumer(condition,number):
    while True:
        condition.acquire()  #acquire自带release功能
        print(f"{number}正在等待condition")
        condition.wait()  #等待条件被满足（阻塞等到notify来唤醒进程来重新获取锁），走到这一步时会自动释放锁，但是等notify这个命令执行完后就没有释放锁的功能了，因为wait是一次性判断
        print(f"{number}已释放condition")
        condition.release()

if __name__ == "__main__":
    condition = Condition()
    producer_process = Process(target=producer,args=(condition,))#默认为RLock，若改为Lock由于是互斥锁会导致抢锁时一次只能有一个消费者
    producer_process.start()
    consumers = [
        Process(target=consumer,args=(condition,1)),
        Process(target=consumer,args=(condition,2)),
        Process(target=consumer,args=(condition,3)),
        Process(target=consumer,args=(condition,4)),
        Process(target=consumer,args=(condition,5))
    ]
    for c in consumers:
        c.start()

    producer_process.join()
    for c in consumers:
        c.join()

#锁是停在acquire()方法而条件变量是停在wait()