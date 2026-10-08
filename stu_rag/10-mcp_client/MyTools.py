#注册工具，工具来自于MCP服务器
from mcp_client.MCPClient import call_mcp_tool
def query_weather(city:str) ->dict:
    """
        当用户问题中包含天气查询时，使用该工具，参数city，表示查询天气的城市名称
    """
    return call_mcp_tool(tool_name="query_weather",city =city)