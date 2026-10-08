#在python中，queue模块提供了适用于多线程环境的队列实现（线程的消息队列进程不能使用）
#Queue、LifoQueue（后进先出队列）、PriorityQueue（优先级队列）
#Queue：最常见的队列，使用queue.Queue创建
#queue.Queue(maxsize=0)  注意一定要设置大小
from threading import Thread
from queue import Queue
import time

def process1(thread_queue):
    print("准备接受数据")
    received_data = thread_queue.get()
    print("接收到的数据为：",received_data)

if __name__ =="__main__":
    thread_queue = Queue(5)
    t1 = Thread(target=process1,args=(thread_queue,))
    t1.start()
    time.sleep(2)
    thread_queue.put("hello")

#Queue.qsize(): 返回队列中当前有几条消息。
#Queue.empty(): 如果队列为空，返回 True，否则返回 False。
#Queue.full(): 如果队列已满（达到最大尺寸），返回 True，否则返回 False。
#Queue.put(item, block=True, timeout=None): 将 item 放入队列。如果 block 是 True 且 timeout 是 None（默认），则在必要时阻塞至有空闲的插槽。如果 timeout 是正数，将最多阻塞 timeout 秒，如果在这段时间内没有可用的插槽，将引发 queue.Full 异常。
#Queue.put_nowait(item): 相当于 Queue.put(item, block=False)。如果队列已满，立即引发 queue.Full 异常。
#Queue.get(block=True, timeout=None): 从队列中移除并返回一个元素。如果 block 是 True 且 timeout 是 None（默认），则在必要时阻塞至队列中有项目可用。如果 timeout 是正数，将最多阻塞 timeout 秒，如果在这段时间内没有项目可用，将引发 queue.Empty 异常。
#Queue.get_nowait(): 相当于 Queue.get(block=False)。如果队列为空，立即引发 queue.Empty 异常。
#Queue.task_done(): 指示之前加入的一个任务已经完成。由队列的消费者线程使用。每个 Queue.get() 调用之后，需要调用 Queue.task_done() 告诉队列该任务处理完成，需要get方去使用
#Queue.join(): 阻塞调用线程，直到队列中的所有项目都被处理完（即队列中每个项目都有一个对应的 Queue.task_done() 调用，要用task_done配合着使用
def producer(queue):
    for i in range(5):
        queue.put(f"Product {i}")
        print(f"Produced {i}")
        time.sleep(1)

def consumer(queue):
    while True:
        product = queue.get()
        if product is None:
            queue.task_done()
            break  #接收到结束信号，退出循环
        print(f"Consumed {product}")
        queue.task_done()  #只执行了5次，最后一次传None就跳出循环去了

if __name__ == "__main__":
    queue = Queue(5)
    p = Thread(target=producer,args=(queue,))
    c = Thread(target=consumer,args=(queue,))
    p.start()
    c.start()
    p.join()  #等待生产者线程结束
    queue.put(None)  #发送结束信号给消费者
    c.join()  #等待消费者线程结束
    queue.join()
    print("over")

#LifoQueue：用来实现后进先出的队列，该队列允许最后被放入队列的元素最先取出，使用queue.LifoQueue创建
#Queue.LifoQueue(maxsize=0)，maxsize是队列的最大尺寸，若设置为小于等于0的数，则队列尺寸无限
#PrioityQueue：用来实现优先级队列，在其中元素被赋予一个优先级值，并且元素会按照优先级顺序被去除，使用queue.PriorityQueue来创建
#queue.PriorityQueue(maxsize=0) maxsize是队列的最大尺寸，若设置为小于等于0的数，则队列尺寸无限
#优先级越高的，其优先级数值越小，优先级相同的话，优先取出先放入队列的元素
