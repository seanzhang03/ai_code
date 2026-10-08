#线程池：维护一个工作线程的集合，用于执行任务，当任务到达时，可以选择一个空闲的线程来处理人物为，而不是为每个任务创建一个新的线程
#submit(fn, *args, **kwargs): 提交一个可调用的函数 fn 和必要的参数 args 和 kwargs 到线程池中执行。这个方法返回一个 Future 对象。
#map(func, *iterables, timeout=None, chunksize=1): 它允许你将一个函数 func 应用于多个可选对象 iterables 中的元素，并且并行地在多个线程上执行这些函数调用。
# timeout 是可选参数，用于设置阻塞等待每个任务完成的最大秒数。如果 timeout 被触发，将引发 concurrent.futures.TimeoutError。
# chunksize 是可选参数，用于指定每次切割几个参数给func，不过只对进程池有效果，对线程池无效。返回的结果是一个迭代器。
#shutdown(wait=True): 关闭线程池，停止接收新任务。如果 wait 参数为 True，则等待所有已提交的任务完成。当使用with语句创建线程池时，with语句会在结束后自动调用shutdown。
import threading
from concurrent.futures import ThreadPoolExecutor
def calculate_square(number):
    return number*number
numbers = [1,2,3,4,5,6,7,8,9,10]
with ThreadPoolExecutor(max_workers=5) as executor:
    results = []
    results = executor.map(calculate_square,numbers)
    print(list(results))