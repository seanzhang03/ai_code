from langchain.agents import create_agent
from tools.mysql_tool import mysql_tool
from model.my_model import MyModel
import asyncio
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
            system_prompt=self.prompt
        )
        return self.agent

    #同步聊天
    def chat_invoke(self,question):
        try:
            msg = {"messages":[{"role": "user", "content": question}]}
            rs =self.agent.invoke(msg)
            return rs["messages"][-1].content
        except Exception as e:
            print(f"同步聊天出现异常：{e}")

    #异步聊天
    async def chat_async(self,question):
        try:
            msg = {"messages":[{"role": "user", "content": question}]}
            rs =self.agent.astream_events(msg,version="v2")
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
    rs = agent.chat_invoke("张三的邮箱是多少")
    print(rs)
    #异步测试
    asyncio.run(test_stream("李四的邮箱是多少"))