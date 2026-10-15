from tools.amap_tool import amap_tool
from tools.send_email_tool import send_email_tool
from tools.mysql_tool import mysql_tool
from model.my_model import MyModel

from langchain.agents import create_agent


def get_agent(question):
    #创建大语言模型
    model = MyModel.get_line_model()
    #创建工具
    tools = [mysql_tool,send_email_tool,amap_tool]
    #创建提示词
    prompt = """
    1.角色：你是一个邮件发送助手
    2.任务：
        步骤1：调用工具mysql_tool来查询用户的邮箱
        例如：通知张三今天下午来开会，执行sql语句
        select email from user_info where user_name="张三"
        步骤2：调用工具send_email_tool发送邮件
    """
    #创建智能体或创建代理
    agent = create_agent(
        model=model, #模型
        tools=tools, #工具
        debug=True, #是否开启调试模式，生产环境下关闭
        system_prompt=prompt #提示词
    )
    rs = agent.invoke({
        "messages":[
            {
                "role":"user",
                "content":question
            }
        ]
    })
    return rs["messages"][-1].content

if __name__ == '__main__':
    q="通知用户李四下午来开会"
    q1="成都市宽窄巷子到春熙路怎么走"
    rs = get_agent(q1)
    print(rs)