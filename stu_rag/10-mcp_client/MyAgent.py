from langchain.agents import  create_agent
from langchain_core.messages import AIMessage
from langchain_core.tools import  tool
from pydantic import BaseModel,Field
from langchain_ollama import ChatOllama
from mcp_client.MyTools import query_weather

#langchain1.0开始，智能体导包
from langchain.agents import create_agent

llm = ChatOllama(
    base_url="http://localhost:11434",
    model="qwen2.5:7b",
    streaming=True
)

system_prompt="""
    你是一个有工具调用能力的助手，需要根据用户的问题选择和使用的工具的生成回答或者不选择工具直接回答，规则如下：
    1.你有一个query_weather工具，当用户问题包含天气查询时，使用该工具，参数city，表示查询天气的城市名称，基于工具结果生成友好回复
    2.其他问题，请直接用大模型生成回答
"""

agent = create_agent(
    model=llm, #大模型对象
    tools=[query_weather], #工具列表
    system_prompt=system_prompt,
    debug=True,  #输出执行信息
)

rs = agent.invoke({"messages":"成都的天气怎么样？"})
print(rs)