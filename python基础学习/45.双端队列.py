#双端队列（deque，double-ended queue）：支持在队列的头部和尾部进行插入和删除操作，是一种具有队列和栈的性质的数据结构。
# 双端队列可以在队列的任意一端入队和出队。
#Deque() 创建一个空的双端队列
#add_front(data)  从队头加入一个元素
#add_read(data)  从队尾加入一个元素
#remove_front()  从队头删除一个元素
#remove_read()  从队尾删除一个元素
#is_empty()  判断队列是否为空
#size() 返回队列大小
class Deque:
    def __init__(self):
        self.__list = []

    def add_front(self,data):
        self.__list.insert(0,data)

    def add_rear(self,data):
        self.__list.append(data)

    def remove_front(self):
        return self.__list.pop(0)

    def remove_rear(self):
        return self.__list.pop()


    def is_empty(self):
        return self.__list == []

    def size(self):
        return len(self.__list)

    def display(self):
        print(self.__list)

if __name__ == "__main__":
    deque = Deque()
    deque.add_front(4)
    deque.add_front(3)
    deque.add_front(2)
    deque.add_front(1)
    deque.add_rear(5)
    print(deque.remove_front())
    print(deque.size())
    print(deque.remove_rear())
    deque.display()