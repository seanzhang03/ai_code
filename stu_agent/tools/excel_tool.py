from langchain_core.tools import tool
from pydantic import BaseModel,Field
import pandas as pd
import time
#
class ExcelParams(BaseModel):
        data:dict = Field(...,description="数据，数据格式为{'姓名':['张三','李四','王五'],'部门':['研发部','市场部','财务部'],'工资':[15000,12000,18000]}")
@tool(args_schema=ExcelParams)
def excel_tool(data:dict)->str:
        """
                Excel数据写入
        """
        try:
                #准备数据
                df=pd.DataFrame(data)
                file_name = time.strftime("%Y%m%d%H%M%S",time.localtime())
                #写入文件
                df.to_excel(f"{file_name}.xlsx", index=False)
                print("Excel文件已生成成功")
                return "写入成功"
        except Exception as e:
                print(f"出现异常{e}")
                return "写入失败"


