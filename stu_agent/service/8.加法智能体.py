from http.cookiejar import debug


from model.my_model import MyModel
from tools.add_tool import add_tool
from langchain.agents import create_agent


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
    question = "1+2等于多少"
    rs=get_agent(question)
    print(rs)
