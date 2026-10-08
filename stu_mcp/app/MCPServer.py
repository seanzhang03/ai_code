#MCP服务器，基于FastMCP实现的，核心代码就是定义工具，暴露工具
#其中：
#1.定义工具：指的就是工具的具体实现代码
#2.暴露工具：通过服务器地址让客户端可以调用工具--客户端想要调用工具，必须先建立连接
#导入类
from fastmcp import FastMCP

#创建fastmcp对象
mcp = FastMCP()

#定义的工具--每一个工具都是一个独立的函数--必须是异步函数
@mcp.tool(
    name="query_weather", #工具名称
    description="""
        查询某个指定城市的天气 ，参数city表示城市的名称
    """,  #给开发者看的工具描述、如何调用这个工具在客户端注册这个工具时写
)
async def query_weather(city:str)->dict:
    return {"result":f"{city}天气是阴天"}

#启动MCP服务器
if __name__== "__main__":
    #基于http协议启动
    mcp.run(
        transport="http",  #启动服务器的协议
        host = "localhost",  #服务器地址
        port = 9000,  #服务器端口
        path = "/mcp", #服务器路径---默认值mcp
        show_banner=True, #是否显示Banner
    )