from http.cookiejar import debug

from langchain_core.messages import AIMessage
from model.my_model import MyModel
from tools.send_email_tool import send_email_tool
from langchain.agents import create_agent
from langchain.agents.middleware import before_agent,AgentState,after_agent,before_model,Runtime
from tools.mysql_tool import mysql_tool
import redis
#创建redis链接
conn = redis.StrictRedis(host="localhost",port=6379,db=0)

#最多访问次数
total = 3

@before_agent
def before_power_val(state:AgentState,time:Runtime):
    user_id = state["messages"][0].additional_kwargs["user_id"]
    key =f"power:{user_id}"
    #获取使用次数
    num = conn.get(key).decode()  #decode将默认编码utf-8解码成str
    print(f"使用智能体：{num}次")
    if int(num) >= total:
        raise Exception("达到使用上限")
    return state

@after_agent
def after_power_val(state:AgentState,time:Runtime):
    user_id = state["messages"][0].additional_kwargs["user_id"]
    #定义一个键名
    key = f"power:{user_id}"
    #自增次数
    conn.incr(key)
    print(f"用户使用智能体{conn.get(key).decode()}次")


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
        middleware=[before_power_val,after_power_val],
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

#初始化用户智能体使用次数
def init_agent(user_id):
    #初始化
    key = f"power:{user_id}"
    conn.set(key,0)

if __name__ == '__main__':
    question = "请给2012761893@qq.com，发送一封邮件，通知其今晚来开会"
    q1 = "赌博是什么"
    q2 = "spring框架是什么"
    q3 = "习近平是谁"
    rs=get_agent("你好",2)
    print(rs)
    # init_agent(2)

