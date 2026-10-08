#进程池时一组预先创建的空闲进程（先有进程后有任务，与之前相反），它们等待执行任务，主进程负责将任务分配到进程池中去执行
#进程池可以管理进程的创建和销毁，避免了频繁创建和销毁带来的开销，通过进程池可以轻松实现多任务的并行处理
#multiprocessing.Pool(processes=None,initializer=None,initargs=(),maxtasksperchild=None)
#processes：进程池中的i你成熟，若为None则默认使用系统处理器核心数
#initializer：每个工作进程启动时要执行的可调用对象，默认为None，调用initializer(*initargs)
#initargs：传递给initializer的可变参数元组
#maxtasksperchild：工作进程退出之前可以完成的任务数，完成后用一个新的工作进程来替代原进程，让闲置资源释放，默认为None意味着Pool存在工作进程就会一直存活
#apply(func,args=())：在一个池工作进程中执行func(args,*kwargs)，然后返回 结果，要强调的是该操作不会在所有池工作进程中并执行func函数
#如果要通过不同参数并发执行func函数，必须从不同线程调用p.apply()函数，或使用p.apply_asyn，是阻塞的，aplly很少使用
#apply(func,args=(),kwds={},callback=None)：异步执行函数func。args是传递给func的位置参数元组，kwds是传递给func的关键字参数字典，callback是一个回调函数，当func执行完成后会被调用
#map(func,iterable,chunksize=None)：将iterable里每个元素作为参数传递给func，返回结果列表，类似于内置函数map，但该方法时并行的
#imap(func,iterable,chunksize)：imap与map不同在于，map时所有进程都执行完了再返回结果，而imap则是立即返回一个iterable可迭代对象

#使用ProcessPoolExecutor创建进程池
#concurrent.futures.ProcessPoolExecutor(max_workers=None,mp_context=None,initializer=None,initargs=())
#max_context：指定进程池中可以同时运行的最大进程数，若设置为None或未指定，默认机器处理器数量，最多61
#mp_context：指定多进程上下文，允许选择不同的上下文，如spawn、fork等待
#主要方法：
#submit(fn,*args,**kwargs)：提交一个可调用对象fn到进程池，发牛一个Future对象，该对象的result方法可用来获取结果
#map(func,*iterables,timeout=None,chunksize=1)：允许将一个函数func应用于多个可迭代对象iterables中的元素，并并行在多个进程上执行这些函数调用。
#timeout是可选参数，用来设置阻塞等待每个任务完成的最大秒数，若timeout被触发，将引发concurrent.futures.TimeoutError
#chunksize是可选参数，指定每次提交给进程池的任务数量（每次给几个进程给进程池），一个较大的chunksize可减少进程间通信的开销，但他也会增加内存消耗，因为他会保证更多任务结果，返回结果是迭代器
#shutdown(wait=True)：等待所有进程完成当前任务后关闭进程池，若 wait参数设置为True，进程池会等待所有任务完成，若设置为False，进程池立即返回，不等任务完成，用with语句管理时，with语句结束时自动调用shutdown
from concurrent.futures import ProcessPoolExecutor
import time

def compute_square(n):
    return n * n

if __name__ == "__main__":
    numbers= [1,2,3,4,5]
    results = []
    with ProcessPoolExecutor(max_workers=3) as executor:  #让进程池中有三个空闲进程
        for num in numbers:
            #提交计算任务到进程池
            future = executor.submit(compute_square,num)
            results.append(future)
        for res in results:
            print(res.result())