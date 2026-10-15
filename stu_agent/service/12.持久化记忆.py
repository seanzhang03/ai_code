
from http.cookiejar import debug

from langgraph.checkpoint.postgres import PostgresSaver #持久化记忆库

from model.my_model import MyModel
from tools.add_tool import add_tool
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

load_dotenv()

def get_agent(question):
    #1.创建大语言模型
    model = MyModel.get_line_model()
    #2.创建工具
    tools = [add_tool]
    #3.创建提示词
    prompt="""
    1.角色：你是一个加法运算器
    2.任务：理解用户需求，调用加法运算工具
    """
    #定义数据库链接
    with PostgresSaver.from_conn_string(os.getenv("PG_URL")) as pg:
        #创建数据库
        pg.setup()
        #4.创建智能体或者创建代理
        agent = create_agent(
            model=model,
            tools=tools,#工具
            system_prompt=prompt, #提示词
            # debug=True, #是否开启调试模式，生产环境下关闭
            checkpointer=pg #持久化记忆
        )
        #5.提问
        rs = agent.invoke(
            {"messages":[{
                "role":"user",
                "content":question
            }]},
            {"configurable":{"thread_id":"1"}}  #指定对话线程来找到记忆存储
        )

        return rs["messages"][-1].content

if __name__ == '__main__':
    q1 = "1+2等于多少"
    q2 = "你好，我是谁"
    q3 = "我的第一个是什么"
    q = [
        "1+1等于多少",
        "你好我是谁",
        "我的第一个问题是什么"
    ]
    for i in q:
        rs=get_agent(i)
        print(rs)  #虽然采用了记忆存储，但是仍无法知道第一个问题是什么，因为创建了三个内存，每个对象的记忆是单独的，没有共享
                   #若想解决这个问题，就只能开辟一个内存空间来共享
                   #解决方法：将get_agent的1到4步移出函数内
