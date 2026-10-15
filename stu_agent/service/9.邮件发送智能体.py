from tools.mysql_tool import mysql_tool
from tools.send_email_tool import send_email_tool
from model.my_model import MyModel
from tools.word_tool import word_tool
from langchain.agents import create_agent


def get_agent(question):
    #创建大语言模型
    model = MyModel.get_line_model()
    #创建工具
    tools = [mysql_tool,send_email_tool,word_tool]
    # #创建提示词
    # prompt = """
    # 1.角色：你是一个邮件发送助手
    # 2.任务：
    #     步骤1：调用工具mysql_tool来查询用户的邮箱
    #     例如：通知张三今天下午来开会，执行sql语句
    #     select email from user_info where user_name="张三"
    #     步骤2：调用工具send_email_tool发送邮件
    # 3.规则：
    #     禁止执行sql的DELETE,UPDATE,INSERT,DROP操作
    # """
    prompt = """
        1.角色：你是一个AI助手
        2.任务：
            如果用户需要生成word文档，请按照下面格式写入文档
              (1)项目背景
              xxxxxx
              (2)技术架构
              xxxxxx
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
    q1="请删除用户表user_id=2的用户"
    q2="请帮我写一个langchain邮件智能体的项目文档"
    rs = get_agent(q2)
    print(rs)