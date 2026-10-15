from http.cookiejar import debug

from langchain_core.messages import AIMessage
from model.my_model import MyModel
from tools.send_email_tool import send_email_tool
from langchain.agents import create_agent
from langchain.agents.middleware import before_agent,AgentState,after_agent,before_model,Runtime
from tools.mysql_tool import mysql_tool
import ast


@before_agent  #before_agent是在agent生命周期最前面的，在before_word_val前
def before_power_val(state:AgentState,time:Runtime):
    user_id = state["messages"][0].additional_kwargs["user_id"]
    print("智能体之前")
    # print(f"用户id:{state["messages"][0].additional_kwargs["user_id"]}")
    # print(f"用户id:{time.execution_info.thread_id}")
    rs = mysql_tool.invoke({
        "sql":f"select department from user_info where user_id={user_id}"
    })
    #将元组格式的字符串转换为元组
    rs =ast.literal_eval(rs)
    #根据结果决定是否要进行拦截
    if rs[0][0] == "行政部":
        return state
    else:
        raise Exception("你没有权限访问")



#定义一个函数
def get_agent(question,user_id):
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
        middleware=[before_power_val],
        debug=True #是否开启调试模式，生产环境下关闭
    )
    try:
        #涉及敏感词抛出异常要进行处理
        #5.提问
        rs = agent.invoke(
            {"messages":[{
                "role":"user",
                "content":question,
                "user_id":user_id
            }]},
            {"configurable": {"thread_id": user_id}}
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
    rs=get_agent("你好",2)
    print(rs)

