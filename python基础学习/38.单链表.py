class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class LinkList:
    def __init__(self,node=None):
        #__head是私有属性
        self.__head = node

    def is_empty(self):  #判断链表是否为空
        return self.__head == None

    def length(self):  #链表长度
        current = self.__head  #设置一个游标
        count = 0
        while current !=None:
            count += 1
            current = current.next
        return count

    def travel(self):
        current = self.__head
        while current != None:
            print(current.data,end=' ')
            current = current.next
        print("")

    def add(self,data):  #头插法
        new_node = Node(data)
        new_node.next = self.__head
        self.__head = new_node

    def append(self,data):  #尾插法
        new_node = Node(data)
        if self.is_empty():
            self.__head = new_node
        else:
            current = self.__head
            while current.next != None:  #不包括空链表的清空
                current = current.next
            current.next = new_node

    def insert(self,pos,data):  #pos下角标,即在第几个元素后插入 data要插入的元素
        if pos > self.length():
            self.append(data)
        elif pos<=0:
            self.add(data)
        else :
            new_node = Node(data)
            pre = self.__head
            count = 0
            while count < (pos-1):
                count+= 1
                pre = pre.next
            new_node.next = pre.next
            pre.next = new_node

    def remove(self,data): #删除元素
        current = self.__head
        pre = None
        while current != None:
            if current.data == data:  #判断当前结点元素与要删除的元素是否一样
                if current == self.__head:  #判断结点是否是单链表第一个结点
                    self.__head = current.next
                else:
                    pre.next = current.next
                break  #记得找到元素后要break
            else:
                pre =current
                current = current.next

    def search(self,data):
        current = self.__head
        while current != None:
            if current.data == data:
                return True
            else:
                current = current.next
            return False



if __name__ =="__main__":
    linklist = LinkList()
    print(linklist.is_empty())
    print(linklist.length())
    linklist.add(10)
    linklist.add(20)
    linklist.add(30)
    linklist.append(50) 
    linklist.append(60)
    linklist.travel()
    print(linklist.is_empty())
    print(linklist.length())
    linklist.insert(2,500)
    linklist.insert(-1,123)
    linklist.insert(20,670)
    linklist.travel()
    linklist.remove(500)
    linklist.travel()
    linklist.search(100)
    linklist.search(123)