from http.cookiejar import debug

from langchain_core.messages import AIMessage
from model.my_model import MyModel
from tools.send_email_tool import send_email_tool
from langchain.agents import create_agent
from langchain.agents.middleware import before_model,AgentState,after_model
from langgraph.runtime import Runtime
import re

@before_model
def before_word_val(state:AgentState,time:Runtime):
    print("模型之前调用")
    print(state)
    #获取用户信息
    info = state["messages"][0].content
    #一般来说，要在数据库里查找敏感词，这里仅作模拟
    sensitive_words=["赌博","吸毒","嫖娼"]
    for word in sensitive_words:
        if word in info:
            #抛出异常
            raise Exception("敏感词拦截")
    #没有拦截，返回state
    return state

@after_model()
def after_word_val(state:AgentState,time:Runtime):
    print("模型之后调用")
    print(state)
    sensitive_words = ["习近平", "李强", "李克强"]
    ai_msg = state["messages"][-1].content
    for word in sensitive_words:
        if word in ai_msg:
            new_msg = re.sub(word,"***",ai_msg)  #正则处理敏感信息
            return {"messages":[AIMessage(content=new_msg)]}
    return state

#定义一个函数
def get_agent(question):
    #1.创建大语言模型
    model = MyModel.get_line_model()
    #2.创建工具
    tools = [send_email_tool]
    #3.创建提示词
    prompt="""你是一个邮件发送助手"""
    #4.创建智能体或者创建代理
    agent = create_agent(
        model=model,
        tools=tools,#工具
        system_prompt=prompt, #提示词
        middleware=[before_word_val,after_word_val],
        debug=True #是否开启调试模式，生产环境下关闭
    )
    try:
        #涉及敏感词抛出异常要进行处理
        #5.提问
        rs = agent.invoke(
            {"messages":[{
                "role":"user",
                "content":question
            }]},
            {"configurable": {"thread_id": "6"}}
        )
        return rs["messages"][-1].content
    except Exception as e:
        print(e)
        return e

if __name__ == '__main__':
    question = "请给2012761893@qq.com，发送一封邮件，通知其今晚来开会"
    q1 = "赌博是什么"
    q2 = "spring框架是什么"
    q3 = "习近平是谁"
    rs=get_agent(q3)
    print(rs)

