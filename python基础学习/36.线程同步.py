#屏障：在threading模块中，Barrier是一种同步机制，让一组线程在某个点上同步，当所有线程到达屏障点时，它们将继续执行，若任何线程美亚由到达屏障点，所有线程被阻塞，直到所有线程都到达
#barrier = threading.Barrier(parties,action=None,timeout=None)
#parties：屏障点上需要等待的线程数量
#action：可选参数，当所有线程到达屏障点时，可以执行的一个函数
#timeout：可选参数：默认的超时时间，若wait没有指定时间将使用这个时间，优先级低于wait指定的timeout
#wait(timeout)：阻塞线程，直到屏障被释放。如果所有线程都到达屏障点，屏障将被释放，所有线程继续执行；如果任何线程没有到达，所有线程将被阻塞。如果提供了timeout，这里的timeout会优先于创建Barrier对象时提供的timeout参数。该函数会返回一个整数，取值在0-(parties-1)之间。
#reset()：重置Barrier为默认的初始状态。如果Barrier中仍有线程等待释放，将会引发异常。
#abort()：使Barrier处于破损状态，这将导致任何现有和未来对wait()方法的调用失败并引发异常。屏障就不能使用了
#parties：冲出Barrier所需要的线程数量，可以用来看有几个线程到达了屏障。
#n_waiting：当前时刻正在Barrier中阻塞的线程数量。
#broken：一个布尔值，表示Barrier是否为破损态
import threading
import time
import random
def worker(barrier):
    print(f"Worker {threading.current_thread().name} is waiting for the barrier.")
    seconds = random.randint(0,5)
    print(f"Worker {threading.current_thread().name} is waiting {seconds}.")
    time.sleep(seconds)  #若在全部线程sleep完之前用reset就会抛出异常
    barrier.wait()
    print(f"Worker {threading.current_thread().name} has passed the barrier.")

if __name__ =="__main__":
    barrier =threading.Barrier(5)
    workers=[
            threading.Thread(target=worker,args=(barrier,)),
            threading.Thread(target=worker,args=(barrier,)),
            threading.Thread(target=worker,args=(barrier,)),
            threading.Thread(target=worker,args=(barrier,)),
            threading.Thread(target=worker,args=(barrier,)),
            ]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()