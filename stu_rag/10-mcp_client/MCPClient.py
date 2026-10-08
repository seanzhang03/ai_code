#因为MCP服务器的工具定义是异步的，调用的时候应该用异步的方式来实现
#但是后面的代码都是同步的，所以选择把异步调用转换为同步调用，和后面的代码衔接
#这个过程并不是一定要有，只是针对于当前的场景

#1.导入FastMCP客户端对象
from fastmcp import Client
import asyncio

#2.定义MCP服务器连接地址
MCP_SERVER_URL = "http://localhost:9000/mcp"

#3.写一个函数---封装工具的调用步骤，后期通过这个函数就可以访问MCP服务器上的工具
#tool_name:str，工具名称
#**kwargs:dict，工具参数---无法保证所有的工具的参数都是一样的个数，所以采用可变参数
def call_mcp_tool(tool_name:str,**kwargs):
    #异步调用
    async def async_call_tool():
        #建立连接
        async with Client(MCP_SERVER_URL) as client:
            #调用工具
            return await client.call_tool(tool_name,kwargs)
        #返回工具调用结果
    return asyncio.run(async_call_tool())

if __name__ =="__main__":
    rs=call_mcp_tool(tool_name="query_weather",city="chengdu")
    print(rs)