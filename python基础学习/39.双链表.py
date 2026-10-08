class Node:
    def __init__(self,data):
        self.data = data
        self.next = None
        self.prev = None

class DoubleLinkList:
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
        if self.is_empty():
            self.__head  = new_node
        else:
            new_node = Node(data)
            new_node.next = self.__head
            self.__head = new_node
            new_node.next.prev = new_node

    def append(self,data):  #尾插法
        new_node = Node(data)
        if self.is_empty():
            self.__head = new_node
        else:
            current = self.__head
            while current.next != None:  #不包括空链表的清空
                current = current.next
            current.next = new_node
            new_node.prev = current

    def insert(self,pos,data):  #pos下角标,即在第几个元素后插入 data要插入的元素
        if pos > self.length():
            self.append(data)
        elif pos<=0:
            self.add(data)
        else :
            new_node = Node(data)
            current = self.__head
            count = 0
            while count < pos:
                count+= 1
                current = current.next
            new_node.next = current
            new_node.prev = current.prev
            current.prev.next = new_node
            current.prev = new_node
            

    def remove(self,data): #删除元素
        current = self.__head  #判断当前结点是否为头结点
        while current != None:
            if current.data == data:  #判断当前结点元素与要删除的元素是否一样
                if current == self.__head:  #判断结点是否是单链表第一个结点
                    self.__head = current.next
                    if current.next: #判断链表中头结点是否为唯一的结点
                        current.next.prev = None  #不止有一个结点时，让第二个结点指向None
                else:
                    current.prev.next = current.next
                    if current.next:  #当为非末尾结点时执行下面的，若为末尾结点不执行
                        current.next.prev = current.prev
                break  #记得找到元素后要break
            else:
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
    doublelinklist = DoubleLinkList()
    print(doublelinklist.is_empty())
    print(doublelinklist.length())
    doublelinklist.add(10)
    doublelinklist.add(20)
    doublelinklist.add(30)
    doublelinklist.append(50) 
    doublelinklist.append(60)
    doublelinklist.travel()
    print(doublelinklist.is_empty())
    print(doublelinklist.length())
    doublelinklist.insert(2,500)
    doublelinklist.insert(-1,123)
    doublelinklist.insert(20,670)
    doublelinklist.travel()
    doublelinklist.remove(500)
    doublelinklist.travel()
    doublelinklist.search(100)
    doublelinklist.search(123)
