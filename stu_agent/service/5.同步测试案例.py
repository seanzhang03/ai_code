from model.my_model import MyModel
import time

#定义一个模型同步案例
def test01(user_id,question):
    #开始时间
    start_time = time.time()
    model = MyModel.get_local_model()
    rs = model.invoke(question)
    print(f"用户:{user_id} 结果:{rs.content}")
    #结束时间
    end_time =time.time()
    print(f"用户{user_id}耗时{end_time-start_time:.2f}秒")

#定义一个模拟多个拥有访问同步接口
def main():
    # 开始时间
    start_time = time.time()
    #定义一个问题列表
    q =[
        ("A","什么是langchain"),
        ("B","什么是流式输出"),
        ("C","什么是异步")
    ]
    #模拟三个用户访问
    for x in q:
        test01(x[0],x[1])
    # 结束时间
    end_time = time.time()
    print(f"总耗时{end_time - start_time:.2f}秒")

if __name__ == '__main__':
    main()