#我们直接用agent来实现工具调用，流程：
#1.用户输入问题
#2.agent解析用户的问题，调用工具，基于工具的结果生成回答
from langchain_core.messages import AIMessage
from langchain_core.tools import  tool
from langchain_neo4j.graph_transformers.llm import system_prompt
from pydantic import BaseModel,Field
from langchain_ollama import ChatOllama

class WeatherSchema(BaseModel):
    city:str = Field(...,description="城市名称")

@tool(
    name_or_callable="query_weather",
    description="查询天气的工具函数，参数city，表示查询天气的城市名称",
    args_schema=WeatherSchema,
)
def query_weather(city:str):
    #这里面就是查询天气的逻辑---返回查询结果即可
    print(f"{city}正在被查询天气")
    return f"{city}的天气是晴天" #假设的，没有真正意义上去执行天气查询功能

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
    tools=[ query_weather], #工具列表
    system_prompt=system_prompt,
    debug=True,  #输出执行信息
)

#agent流式输出要加上stream_mode="messages"
for chunk in agent.stream({"messages":"介绍3个成都的美食"},stream_mode="messages"):  #stream_mode必须加上
    print(chunk)
