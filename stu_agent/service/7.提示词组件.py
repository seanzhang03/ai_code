from langchain.agents import create_agent
from model.my_model import MyModel

#一个完成的提示词由以下几个部分组成:
# System Prompt:实体的属性描述以及功能描述等等，规定ai的身份、能力、规则
# Human Prompt:问的问题等
# AI Response:AI的回答
# 上面就构成了一个上下文信息
def get_agent(question):
    model = MyModel.get_line_model()
    tools = []
    # prompt = """
    # 你是一个AI助手
    # """
    prompt = """
    你是一个拥有10年经验的java高级工程师
    要求：1.500字以内
    2.举一个案例
    3.最后总结
    """
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt
    )
    rs = agent.invoke({"messages":[{"role":"user","content":question}]})
    print(rs["messages"][-1].content)

if __name__ == '__main__':
    question = "介绍一下Langchain"
    get_agent(question)