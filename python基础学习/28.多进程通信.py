#管道
#使用multiprocessing.Pipe()可创建一个管道，函数返回一个由两个连接对象组成的元组，这两个对象分别代表管道的两端
#默认情况，管道是双向的，每个端点都可读写
#特点：双向通信，允许2个方向的通信，每个管道有一个接收端和发送端。点对点连接，通常用于2个进程间直接通信，不支持多个进程间的通信
#管道大小有限，其缓冲区是有限的，若缓冲区满了则发送操作要阻塞
#send(obj)：发送一个对象到管道另一端，该对象要是可序列化的
#recv()：从管道另一端接受一个对象，该方法是阻塞的
#close()：关闭管道连接，不需要管道时用该方法释放资源

import multiprocessing
import time
'''
def send_data(pipe):
    time.sleep(2)
    pipe.send("Hello from parent")
def receive_data(pipe):
    print("Child is waiting to receive data...")
    data = pipe.recv()  #阻塞等待
    print(f"Child received: {data}")

if __name__ == "__main__":
    parent_pipe,child_pipe = multiprocessing.Pipe()  #创建管道
    child_process = multiprocessing.Process(target=receive_data,args=(child_pipe,))
    child_process.start()
    send_data(parent_pipe)
    child_process.join()
'''

'''
#消息队列
#提供了一种在进程间传输数据的方式，这种方式是通过在内核中维护一个消息队列来实现的。
#进程可以发送数据到队列，也可以从队列中接受数据，在multiprocessing模块中，Queue类提供了一个先进先出(FIFO)的消息队列
#使用方法：
#queue = Queue(maxsize=10) maxsize为队列中最多可以存放的元素数量
#消息队列的方法
#put(obj,block=True,timeout=None)：将obj放入队列，如果可选参数block是True且timeout是None，就阻塞当前进程，直到有空的缓冲槽
#如果timeout是整数，将会在阻塞了最多timeout秒后还是没有可用的缓冲槽时抛出异常。如果block是False，那么在没空的缓冲槽时立即抛出异常，timeout会被忽略
#get(block=True,timeout=None)：从消息队列里获取信息，该方法为阻塞等待的方法，block和timeout的作用与put一致
#empty()/full()；返回布尔值判断是否为空或为满
#qsize()：返回队列中当前元素的数量
#get_nowait()：立即尝试从队列中获取一个元素，若队列为空，抛出Queue.Empty异常
#put_nowait()：立即尝试向队列里放入一个元素，若队列为满，抛出Queue.Full异常
from multiprocessing import Process,Queue
import time
def process1(process_queue):
    print("准备接受数据")
    print("接收到的数据为：",process_queue.get())  #一次get操作得到一个数据

if __name__ == '__main__':
    process_queue = Queue(5)
    p1 = Process(target = process1,args=(process_queue,))
    p1.start()
    time1 = time.time()
    time.sleep(2)  #在等待的时候子程序已经在执行了
    process_queue.put("hello")
    print(time.time()-time1)
    p1.join()
    p1.close()
    
#注意：
#不要在多个进程间共享同一个队列实例，要给每个进程创建单独的队列实例
#未指定队列大小，将默认为为无限大，可能会导致内存问题，特别是生产者产生消息速度远大于消费者消费消息的速度
#处理队列异常：当队列操作失败（队列满或空），应捕获并处理相应异常
#队列性能：队列操作可能会影响性能，尤其在高并发环境下
'''
'''
#共享内存是一种进程间通信(IPC)机制，即它允许多个进程访问同一块内存空间，每个进程都可以读取或写入这块内存
#共享内存分为变量共享和数组共享，可以解决父子进程间全局变量不共享的情况
#共享变量方法：
#multiprocessing.Value(type_code,*args,lock=True)
#type_code表示类型代码，*args表示初始化变量的值，lock是锁，默认会创建一个锁来保护共享变量
#若传入False，Value的实例就不会被锁保护，将不是进程安全的，最好不要改默认为True
#共享数组方法：
 #multiprocessing.Array(type_code,size_or_initializer,lock=True)
#type_code表示类型代码，size_or_initializer表示数组大小或初始化值，如果是整数，表示数组长度，且数组给初始化为0
 #若是一组序列，则就是数组的初始化值，长度决定数组的长度，lock表示锁
 #共享内存特点
 #高效数据共享，共享内存比其他IPC机制更高效，因为避免了数据的复制
 #同步问题：共享内存要同步机制（如锁）来防止竞态条件
 #类型限制：共享内存数据类型有限，通常只能为基本数据类型
from multiprocessing import Process,Queue
def func(shared_num,shared_array):
    shared_num.value+=1
    for i in range(len(shared_array)):
        shared_array[i]+=1

if __name__ =='__main__':
    shared_num=multiprocessing.Value('i',0)
    shared_array= multiprocessing.Array('i',range(10))
    p=Process(target=func,args=(shared_num,shared_array))
    p.start()
    p.join()
    print(shared_num.value)
    print(shared_array[:])
    '''

#操作共享内存的缓冲区
from multiprocessing import shared_memory
shm = multiprocessing.shared_memory.SharedMemory(name='aaa',create = True,size=10)  #create代表没有共享内存时是否开辟
print(shm)
for i in shm.buf:
    print(i)
value = shm.buf
#value[:3] = 1  #不能一次修改多个
value[1]=1
print(list(value))  

#通过共享内存读写来实现进程间通信
import time
from multiprocessing import shared_memory,Process
def writer(shared_mem_name,size):
    shm = shared_memory.SharedMemory(name=shared_mem_name,create=False)
    buffer = shm.buf
    for i in range(size):
        buffer[i] = i
    print("数据已写入")
    shm.close()  #close只是关闭了接口，并没有清空共享内存

def reader(shared_mem_name,size):
    shm = shared_memory.SharedMemory(name=shared_mem_name,create=False)
    buffer = shm.buf
    data = list(buffer[:size])  #要将缓冲区的内容强转为列表，才能写入
    print("我读到的数据是：",data)
    shm.close()
    shm.unlink()  #作为最后一个使用共享内存的进程，要用unlink销毁共享内存

if __name__== '__main__':
    size=10
    shm = shared_memory.SharedMemory(create=True,size=size)
    write_process = Process(target=writer,args=(shm.name,size))
    write_process.start()
    time.sleep(2)  #加入时延，保证是先写后读，否则可能导致先读后写
    read_process = Process(target=reader,args=(shm.name,size))
    read_process.start()    
    write_process.join()
    read_process.join()
   