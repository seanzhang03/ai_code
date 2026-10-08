#定时器Timer：允许一定时间后执行一个函数或者可调用的对象，Timer类是Thread类的一个子类，因此其具有线程所有特性（即所有内容），可在后台执行定时任务
#class threading.Timer(interval,function,args=None,kwargs=None)
#interval:一个浮点数或整数，表示执行function之前所需要等待的时间
#function：一个可调用的对象，定时器到期时将被执行
#args：传递给function的位置参数元组
#kwargs：传递给function的关键字参数字典
#实例方法
#start()：启动定时器，Timer将在指定时间间隔后开始执行目标函数
#cancel()：取消定时器，若定时器尚未启动，则该方法无效，若定时器正在运行，调用cancel()将停止定时器，并且目标函数不会被调用
import threading
import time 



def get_time():
    current_time = time.time()
    formatted_time = time.strftime("%Y-%m-%d-%H:%M:%S",time.localtime(current_time))
    print(formatted_time)

if __name__ == "__main__":
    timer = threading.Timer(5,get_time)  #计时结束后执行的函数
    timer.start()
    print("Do some other things...")
    timer.join()  #等待定时器的完成



def get_time():
    current_time = time.time()
    formatted_time = time.strftime("%Y-%m-%d-%H:%M:%S",time.localtime(current_time))
    print(formatted_time)
    timer1 = threading.Timer(5,get_time)  #主线程调用了一次get_time的线程，由于没有cancel或join会导致一直递归调用
    timer1.start()
    print(timer1)

if __name__ == "__main__":
    timer = threading.Timer(5,get_time)  #计时结束后执行的函数
    print(timer)
    timer.start()
    print("Do some other things...")
    time.sleep(100)
    timer.join()  #等待定时器的完成
    print(123)  #主线程中调用完一次计时器后并不影响主线程的继续执行，会直接往下继续执行,即第一个5s执行完后执行打印语句
