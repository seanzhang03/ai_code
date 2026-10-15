from http.cookiejar import debug

from langchain_core.messages import HumanMessage

from model.my_model import MyModel
from tools.send_email_tool import send_email_tool
from langchain.agents import create_agent

def get_agent(question):
    #1.创建大语言模型
    model = MyModel.get_line_model()
    #2.创建工具
    tools = [send_email_tool]
    #3.创建提示词
    prompt="""
    你是一个邮件发送助手
    """
    #4.创建智能体或者创建代理
    agent = create_agent(
        model=model,
        tools=tools,#工具
        system_prompt=prompt, #提示词
        #debug=True #是否开启调试模式，生产环境下关闭
    )
    #5.提问
    for c in agent.stream(
        {"messages":[{"role":"user","content":question}]},
        stream_mode="messages"  #流式返回，智能体需要写，模型输出可以不用直接写
    ):
        print(c[0].content,end="")#不换行

#大模型流式输出
def test_model(q):
    model = MyModel.get_line_model()
    #流式输出
    for c in model.stream(q):
        if c.content:
            print(c.content,end="")
        else:
            print("正在思考~~")

if __name__ == '__main__':
    question = "请给2012761893@qq.com，发送一封邮件，通知其今晚来开会"
    rs=get_agent(question)
    print(rs)
    test_model("给我写一个一百字作文，围绕春天为主题")