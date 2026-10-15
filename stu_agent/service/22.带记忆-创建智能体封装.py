from langchain.agents import create_agent
from tools.mysql_tool import mysql_tool
from model.my_model import MyModel
import asyncio
from pggressql_manager.pggressql_manager import pg_saver
'''
    创建不带记忆的智能体封装
'''

class MysqlAgent:
    def __init__(self):
        self.model = MyModel.get_line_model()
        self.prompt =None
        self.tool =None
        self.get_prompt()
        self.get_tool()
        self.get_agent()

    #加载提示词
    def get_prompt(self):
        self.prompt="""
        1.你是一个sql问答助手
        """

    #加载工具
    def get_tool(self):
        #建议用mcp来封装
        self.tool = [mysql_tool]

    #加载智能体
    def get_agent(self):
        self.agent = create_agent(
            model=self.model,
            tools=self.tool,
            checkpointer=pg_saver,  #引入记忆管理
            system_prompt=self.prompt
        )
        return self.agent

    #同步聊天
    def chat_invoke(self,question,user_id):
        try:
            msg = {"messages":[{"role": "user", "content": question}]}
            #构建记忆配置
            config = {"configurable":{"thread_id":user_id}}
            rs =self.agent.invoke(msg,config)
            return rs["messages"][-1].content
        except Exception as e:
            print(f"同步聊天出现异常：{e}")

    #异步聊天
    async def chat_async(self,question):
        try:
            msg = {"messages":[{"role": "user", "content": question}]}
            config = {"configurable": {"thread_id": user_id}}
            rs =self.agent.astream_events(msg,config,version="v2")
            async for event in rs:
                #获取事件类型
                event_type = event["event"]
                if event_type =="on_tool_start":
                    yield f"\n开始执行工具:{event["name"]}\n"
                if event_type =="on_tool_end":
                    yield f"\n工具:{event["name"]} 执行完毕\n"
                if event_type =="on_chat_model_stream":
                    if event["data"]["chunk"].content:
                        yield f"\n{event["data"]["chunk"].content}\n"
        except Exception as e:
            print(f"异步聊天出现异常：{e}")
            yield "异步聊天出现异常"

#测试流式输出
async def test_stream(question):
    agent =MysqlAgent()
    async for data in agent.chat_async(question):
        print(data,end="")

if __name__ == '__main__':
    #同步测试
    agent =MysqlAgent()
    q = [
        "1+1等于多少",
        "你好我是谁",
        "我的第一个问题是什么"
    ]
    for x in q:
        rs = agent.chat_invoke(x,3)
        print(rs)
    # #异步测试
    # asyncio.run(test_stream("李四的邮箱是多少"))

    #Checkpointer保存agent的运行状态(State)
    #四层记忆保存Agent需要理解的用户信息(Memory)，四层记忆是用来记住重要信息
    #四层记忆：
    #1.临时记忆(窗口记忆)：最近的几十轮信息，用redis存储
    #2.摘要记忆：对重要的内容进行浓缩摘要，用postgresql存储
    #3.长期记忆：记住用户最突出的特点，用向量数据库存储
    #4.用户画像：记住用户的基本信息，比如用户是谁？，用redis存储