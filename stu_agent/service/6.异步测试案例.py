import asyncio

from model.my_model import MyModel
import time

#定义一个模型异步案例
async def test01(user_id,question):
    #开始时间
    start_time = time.time()
    model = MyModel.get_local_model()
    rs =await model.ainvoke(question)
    print(f"用户:{user_id} 结果:{rs.content}")
    #结束时间
    end_time =time.time()
    print(f"用户{user_id}耗时{end_time-start_time:.2f}秒")

#定义一个模拟多个拥有访问同步接口
async def main():
    # 开始时间
    start_time = time.time()
    #定义一个问题列表
    q =[
        test01("A","什么是langchain"),
        test01("B","什么是流式输出"),
        test01("C","什么是异步")
    ]
    #模拟三个用户访问，不能再用for循环，for循环是针对同步
    await asyncio.gather(
        *q
    )
    # 结束时间
    end_time = time.time()
    print(f"总耗时{end_time - start_time:.2f}秒")

if __name__ == '__main__':
    asyncio.run(main())