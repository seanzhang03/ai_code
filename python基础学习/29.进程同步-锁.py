#进程同步是指在多进程环境下协调各个进程对共享资源的访问，主要解决的问题是当多个进程并发访问共享资源时，如何保证任意时刻只有一个进程能访问该资源
#从而避免由于进程间的无序竞争导致的系统资源冲突，确保系统的稳定运行
#临界资源是指一段时间内仅允许一个进程访问的资源，这可能是硬件资源，也可能是软件资源如变量、数据、表格、队列等
#临界区是指访问临界资源的那部分代码，在进入临界区之前，需要检查是否可以访问临界资源，确保资源的互斥访问
#进程同步机制
#空则让进：若临界资源处于空闲状态，则进程可以进入其临界区。
#忙则等待：若临界资源正被使用，请求访问的进程要等待

#锁：一种用于控制多个进程访问共享资源的机制，目的是防止多个进程同时访问共享资源时产生的竞态条件，确保了数据的一致性和完整性
#最常用的锁为互斥锁和递归锁

#互斥锁：确保同一时间只有要给进程可以访问资源。当进程正在使用资源时，会锁定该资源，其他进程必须等待锁释放后才能访问
#在multiprocessing模块中，Lock对象可用来确保临界区代码的互斥执行
#使用方法
#acquire(blocking=True,timeout=-1) 
#若blocking为True且timeout是默认值-1，该方法会阻塞直到锁被获取，若blocking为False，则立即返回不阻塞
#release()释放锁
import time
import multiprocessing
from multiprocessing import current_process,Process
def task(lock,queue,amount):
    while True:
        lock.acquire() #获取锁，这把锁被其中一个进程获取后，其他进程无法获取 
        money=queue.get()
        if money>=amount:
            money-=amount
            print(f"{current_process().name}取了{amount}，现在还有{money}")
        else:
            print(f"{current_process().name}取钱失败，银行没钱了")
            lock.release()  #解锁
            queue.put(money)
            break
        queue.put(money)
        time.sleep(1)
        lock.release()  #一定要有释放锁的步骤，不然会造成死锁，导致其他进程无法获取锁

if __name__ =="__main__":
    count = 1000 #初始余额
    queue = multiprocessing.Queue(5)
    queue.put(count)
    lock = multiprocessing.Lock()
    t1 = multiprocessing.Process(target=task,args=(lock,queue,50),name="张三")
    t2 = multiprocessing.Process(target=task,args=(lock,queue,100),name="李四")
    t1.start()
    t2.start()  #让两个进程同时去抢占一个锁，执行完了再去释放锁
    t1.join()
    t2.join()



from multiprocessing import Queue,Lock
def producer(queue):
    while True:
        for i in range(5):
            queue.put("hello")
        time.sleep(2)

def consumer(queue,lock):
    while True:
        lock.acquire()  #获取锁，确保消费数据的进程不会被其他消费者进程打断
        if not queue.empty():
            res = queue.get()
            print(f"{current_process().name}:{res}")
        lock.release()

if __name__ == "__main__":
    queue = Queue(10)
    lock = Lock()  #将互斥锁改成递归锁只需要把这里改成RLock，改完后将release删掉就不会造成死锁，但是会造成该进程循环执行
    producer_process = Process(target = producer,args=(queue,))
    producer_process.start()
    consumer1_process = Process(target=consumer,args=(queue,lock),name="consumer1")
    consumer1_process.start()
    consumer2_process = Process(target=consumer,args=(queue,lock),name="consumer2")
    consumer2_process.start()
    consumer3_process = Process(target=consumer,args=(queue,lock),name="consumer3")
    consumer3_process.start()
    consumer4_process = Process(target=consumer,args=(queue,lock),name="consumer4")
    consumer4_process.start()
    consumer5_process = Process(target=consumer,args=(queue,lock),name="consumer5")
    consumer5_process.start()
    consumer1_process.join()
    consumer2_process.join()
    consumer3_process.join()
    consumer4_process.join()
    consumer5_process.join()

#死锁：多个进程之间，每个都在等待其他进程释放资源，但是这些资源又被其他进程持有，导致所有进程都无法继续执行，形成了一种僵持状态
#即多个进程因为竞争资源而造成的互相等待的局面
#1. 互斥条件（Mutual Exclusion）资源不能被多个进程同时使用，即资源在一段时间内只能被一个进程占用。
#2. 占有和等待条件（Hold and Wait）进程至少持有一个资源，并且正在等待获取额外的资源，而该资源当前被其他进程持有。
#3. 不可抢占条件（No Preemption）已经分配给进程的资源，在该进程完成任务之前不能被强行抢占。
#4. 循环等待条件（Circular Wait）存在一种进程资源的循环等待链，链中的每个进程至少持有一个资源，并等待获取下一个进程所持有的资源
#锁的释放和锁的获取都可以被with语句进行管理
#lock.acquire()和lock.release()两个语句可以被一个with lock: 给替代

#递归锁（可重入锁）：与互斥锁不同，递归锁允许同一进程多次获取同一把锁，即一个进程获取了锁，还可以再次获取锁但不导致死锁
#该锁内部有一个计数器，当一个进程获取到锁时，计数器会增加，当进程释放锁时，计数器会减少，
# 只有计数器为0时，锁才会真正释放，才允许其他进程去获取锁，其他使用与互斥锁一致
#递归锁应用场景（可重用性）：递归函数、递归操作、递归数据库操作、递归网络操作、递归图形处理、递归算法、递归数据结构访问

#信号量：更高级的同步机制，内部维护着一个计数器，用于控制对共享资源的最大并发访问数量。
#信号量使用方法
#multiprocessing.Semaphore(value=1)：创建一个信号量对象，value指定初始可用数量，即可被几个进程访问，默认为1
#相关方法
#acquire([timeout=None])：尝试获取信号量，若信号量可用，则其值减一并返回True，若不可用，阻塞到超时或信号量变为可用
#若没指定timeout或timeout为None，就一直等待到信号量可用
#release()：释放一个信号量，其值加一，若信号量之前被阻塞，就会唤醒一个正在等待的进程
#PV操作：进程同步中的一种基本机制，也叫信号量机制，用来解决同步问题，特别是临界区问题
#P操作（测试和等待操作，也叫wait操作）：该操作检查信号量的值（是否有空余），若信号量值大于0，就将其-1，若信号量为0，则该进程被挂起，直到信号量值变为正数
#V操作（信号操作，也叫signal操作）：该操作会增加信号量的值，若信号量的值增加后仍小于等于0，则会唤醒一个因P操作而被挂起的进程。


