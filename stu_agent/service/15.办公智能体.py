from http.cookiejar import debug

from model.my_model import MyModel
from tools.mysql_tool import mysql_tool
from tools.excel_tool import excel_tool
from tools.pdf_tool import pdf_tool
from tools.txt_tool import txt_tool
from langchain.agents import create_agent

#agent工作原理：
# 1.LLM理解用户意图
# 2.判断是否需要调用tool
# 3.若为是，进行tool calling，tool执行完成后返回给observation，再给reasoning，最后给final answer
#定义一个函数
def get_agent(question):
    #1.创建大语言模型
    model = MyModel.get_line_model()
    #2.创建工具
    tools = [mysql_tool,excel_tool,pdf_tool,txt_tool]
    #3.创建提示词
    prompt="""
    你是一个办公助手
    """
    #4.创建智能体或者创建代理
    agent = create_agent(
        model=model,
        tools=tools,#工具
        system_prompt=prompt, #提示词
        debug=True #是否开启调试模式，生产环境下关闭
    )
    #5.提问
    rs = agent.invoke(
        {"messages":[{
            "role":"user",
            "content":question
        }]}
    )

    return rs["messages"][-1].content

if __name__ == '__main__':
    question = "请查询用户表所有数据，把数据写入到excel中"
    q1 = "请帮我写一个文章，解释什么是langchain，包含以下内容：1.技术介绍 2.组件介绍 写入到pdf文件里"
    q2 = "请帮我写一个文章，解释什么是spring boot，包含以下内容：1.技术介绍 2.组件介绍 写入到txt文件里"
    rs=get_agent(q2)
    print(rs)
