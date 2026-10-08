#队列(Queue)：也是一种基本的数据结构，在队列中的插入和删除都遵循先进先出（First in First out，FIFO）的原则。
#元素可以在任何时刻从队尾插入，但是只有在队列最前面的元素才能被取出或者删除。
#通常将队列中允许插入的一端称为队尾，将允许删除的一端称为队头。队列不允许在中间部位进行操作！
#Queue()  创建一个空的队列
#is_empty()  队列是否为空
#enqueue(data)  从队列尾添加一个元素
#dequeue(data)  从队列头移除并返回第一个元素
#size()  返回队列的大小
class Queue():
    def __init__(self):
        self.__list = []

    def is_empty(self):
        return self.__list == []

    def enqueue(self,data):
        self.__list.append(data)

    def dequeue(self):
        return self.__list.pop(0)

    def size(self):
        return(self.__list)

if __name__ == "__main__":
    queue = Queue()
    queue.enqueue(10)
    queue.enqueue(50)
    queue.enqueue(100)
    print(queue.size())
    print(queue.dequeue())
    print(queue.size())
    print(queue.is_empty())


