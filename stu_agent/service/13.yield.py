from model.my_model import MyModel
from tools.send_email_tool import send_email_tool
from langchain.agents import create_agent
import asyncio
#定义一个函数
async def get_agent(question):
    #1.创建大语言模型
    model = MyModel.get_line_model()
    #2.创建工具
    tools = [send_email_tool]
    #3.创建提示词
    prompt = """
        你是一个邮件发送助手
    """
    #4.创建智能体
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt,
    )
    #不会影响下面走，只是暂停函数
    yield "正在思考~"
    #5.提问
    async for c,m in agent.astream(
            {"messages":[{"role":"user","content":question}]},
            stream_mode="messages"
    ):
        if c.content:
            # print(c.cotent,end="")
            yield c.content

if __name__ == '__main__':
    q="你好，请帮我写200字关于春天的作文"
    #创建一个异步迭代器或者协程函数
    async def get_result(question):
        async for i in get_agent(question):
            print(i)
    #异步调用函数
    rs = asyncio.run(get_result(q))
    print(rs)