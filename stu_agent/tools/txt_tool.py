from pydantic import BaseModel,Field
from langchain.tools import tool
import time

class TextParams(BaseModel):
    content:str = Field(...,description="txt内容")

@tool(args_schema=TextParams)
def txt_tool(content:str)->str:
    """
    txt文件写入
    """
    try:
        file_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
        with open(f"{file_name}.txt","w",encoding="utf-8") as f:
            f.write(content)
        return "txt文件写入成功"
    except Exception as e:
        print(f"出现异常{e}")
        return "txt文件写入失败"