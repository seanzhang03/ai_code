from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from numba.scripts.generate_lower_listing import description
from pydantic import BaseModel,Field


#定义工具直接使用@tool装饰器即可，参数：
#1.name_or_callable:工具的名称，不写就是函数名字
#2.description：工具的描述，告诉模型什么时候调用这个工具或数据库表的信息等
#3.args_schema：参数校验类
#注意事项：如果你不写description参数也可以，那么你就写上函数的注释
#即在函数第一行开始写注释，注释的内容和description一样

#校验天气查询工具参数city的类
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

llm = ChatOllama(
    base_url="http://localhost:11434",
    model="qwen2.5:7b",
    streaming=True
).bind_tools([query_weather])  #绑定工具，参数是一个列表，值为工具名称

#查询成都的天气---解析问题，得到调用哪一个工具以及参数信息
rs = llm.invoke("成都今天的天气怎么样？")
print(rs)
#我们需要把输出过程的内容保存起来，最后把所有的输出信息送给LLM生成最后的答案
messages = []
messages.append(rs)

#工具映射字典
tool_map = {
    "query_weather":query_weather
}

#真正意义上去执行工具
tools_calls=rs.tool_calls
#tool_calls是LLM解析当前问题得到的工具调用列表，我们需要逐个去执行工具，得到每一个结果，保存结果
#执行工具的时候，工具的参数就是tool_calls取出来的内容
for tool_call in tools_calls:
    #工具名称
    tool_name = tool_call.get("name","")
    print(tool_name)
    #执行工具调用，得到工具调用结果
    #tool_result = tool_map[tool_name].invoke(tool_call)
    tool_result = eval(tool_name).invoke(tool_call)
    print(tool_result)
    #把工具调用结果保存下来
    messages.append(tool_result)

#LLM生成最后的回答
final_answer = llm.invoke(messages)
print(final_answer)