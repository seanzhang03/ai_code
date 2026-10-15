from http.cookiejar import debug

from model.my_model import MyModel
from tools.send_email_tool import send_email_tool
from tools.mysql_tool import mysql_tool
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware  #限制调用次数，人工审核中间件
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

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
    middleware=[HumanInTheLoopMiddleware(interrupt_on={
                    "send_email_tool":{
            "allowed_decisions":["approve","reject","edit"],
            "description":"发送邮件需要审核"
    }
    },
            description_prefix="[人工审核]"  #公共提示前缀
    )], #添加中间件
    #debug=True #是否开启调试模式，生产环境下关闭
)
def get_agent(question):
    #5.提问
    rs = agent.invoke(
        {"messages":[{
            "role":"user",
            "content":question
        }]},
        {"configurable":{"thread_id":"5"}}  #加了记忆一定要记得配置
    )
    status_info = rs.get("__interrupt__")
    #判断是否被中断
    if status_info:
        print("==", status_info)
        print("请选择操作：")
        print("   1. approve - 批准发送")
        print("   2. edit - 编辑内容后发送")
        print("   3. reject - 拒绝发送")
        choice = input("请输入你的选择：")
        if choice == "1":
            print("已批准，正在发送邮件...")
            result = agent.invoke(
                Command(resume={
                    "decisions":[{"type":"approve"
                                  }]
                }),
                {"configurable": {"thread_id": "5"}}  #invoke配置
            )
            print(result)
        elif choice == "2":
            to_email = input("请输入收件人邮箱:")
            subject = input("请输入邮件标题")
            content = input("请输入邮件内容:")
            #构建编辑后的参数，这里的参数要和调用的工具里校验的参数名一致
            edited_args = {
                "to_email":to_email,
                "subject":subject,
                "content":content
            }
            final_result = agent.invoke(
                Command(resume={"decisions":[{"type":"edit","edited_action":{
                    "name":"send_email_tool",
                    "args":edited_args
                }}]}),
                {"configurable": {"thread_id": "5"}}
            )
            print("邮件内容已编辑并发送")
            print(final_result["messages"][-1].content)
        else:
            reason = input("请输入拒绝原因:").strip()
            final_result = agent.invoke(
                Command(resume={"decisions":[{"type":"reject","reason":reason}]}),
                {"configurable": {"thread_id": "5"}}
            )
            print("邮件已被拒绝发送")
            print(final_result["messages"][-1].content)

    return rs["messages"][-1].content

if __name__ == '__main__':
    q="请给2012761893@qq.com，发送一封邮件，通知其今晚来开会"
    rs = get_agent(q)
    print(rs)
