from http.cookiejar import debug

from langchain_core.messages import HumanMessage

from model.my_model import MyModel
from tools.send_email_tool import send_email_tool
from tools.mysql_tool import mysql_tool
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware  #限制调用次数，内置的模型中间件
from langgraph.checkpoint.memory import InMemorySaver

#1.创建大语言模型
model = MyModel.get_line_model()
#2.创建工具
tools = [send_email_tool,mysql_tool]
#3.创建提示词
prompt="""1.角色：你是一个邮件发送助手
    2.任务：
        步骤1：调用工具mysql_tool来查询用户的邮箱
        例如：通知张三今天下午来开会，执行sql语句
        select email from user_info where user_name="张三"
        步骤2：调用工具send_email_tool发送邮件
    3.规则：
        禁止执行sql的DELETE,UPDATE,INSERT,DROP操作"""
#4.创建智能体或者创建代理
agent = create_agent(
    model=model,
    tools=tools,#工具
    system_prompt=prompt, #提示词
    checkpointer=InMemorySaver(),
    middleware=[ModelCallLimitMiddleware(
        thread_limit=2, #限制模型调用次数，不是你对话的次数，因为就算是一次对话，调用工具也仍然会导致多次模型调用
        exit_behavior="end" #是否结束会话
    )], #添加中间件
    debug=True #是否开启调试模式，生产环境下关闭
)
def get_agent(question):
    #5.提问
    rs = agent.invoke(
        {"messages":[{
            "role":"user",
            "content":question
        }]},
        {"configurable":{"thread_id":"4"}}  #加了记忆一定要记得配置
    )
    return rs["messages"][-1].content

if __name__ == '__main__':
    question = "请给2012761893@qq.com，发送一封邮件，通知其今晚来开会"
    q = [
        "请给李四，发送一封邮件，通知其今晚来开会",
        "你好，我是sz",
        "我是谁"
    ]
    for x in q:
        rs = get_agent(x)
        print(rs)

