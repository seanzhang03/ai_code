#线性表：有序数据集合
#栈（stack）：又名堆栈，它是一种运算受限的线性表，是一种容器，可存入数据元素、访问元素、删除元素，它的特点在于只能允许在容器的一端（成为栈顶top），进行存入数据（push）和输出数据（pop）的运算，没有位置概念，
# 保证任何时候都可以访问、删除元素。栈仅允许在栈顶一端进行操作，因此，栈是按照先进4后出（LIFO，Last In First Out）的原理进行运作
#push(data) 将data压入栈
#pop() 将栈顶数据移除并返回
#peek() 查看栈顶元素，但未弹出
#is_empty() 检查栈是否为空
#size() 获取栈的大小
class Stack:
    def __init__(self):
        self.__list = []  #构造容器，构建成私有属性

    def push(self,data):
        self.__list.append(data)

    def pop(self):
        if not self.is_empty():
            return self.__list.pop()
        else:
            return None

    def peek(self):
        if not self.is_empty():
            return self.__list[-1]
        else:
            return None


    def is_empty(self):
        return self.__list == []

    def size(self):
        return len(self.__list)

if __name__ == "__main__":
    S = Stack()
    S.push(10)
    S.push(20)
    S.push(30)
    S.push(40)
    print(S.size())
    print(S.peek())
    print(S.size())
    print(S.pop())
    print(S.size())
    print(S.is_empty())