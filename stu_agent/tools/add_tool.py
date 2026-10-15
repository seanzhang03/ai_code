from langchain.tools import tool

@tool  #省略默认拿函数名作为工具名字
def add_tool(a:int,b:int)->str:
    """
    加法运算
    :param a: 加法第一个数
    :param b: 加法第二个数
    :return: 和
    """
    return str(a+b)