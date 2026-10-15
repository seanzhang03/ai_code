import time

from fpdf import FPDF
import os
from pydantic import BaseModel,Field
from langchain.tools import tool
import os

def find_chinese_font():  # 1 个用法 新 *
    """返回第一个可用的中文字体文件路径，找不到则返回 None"""
    # 常见 Windows 中文字体路径（按优先级别）
    candidates = [
        r"C:/Windows/Fonts/simhei.ttf",   # 黑体
        r"C:/Windows/Fonts/simsun.ttc",   # 宋体
        r"C:/Windows/Fonts/msyh.ttf",     # 微软雅黑
        r"C:/Windows/Fonts/msyhbd.ttf",   # 微软雅黑粗体
        r"C:/Windows/Fonts/simkai.ttf",   # 楷体
    ]

    for path in candidates:
        if os.path.exists(path):
            return path
    return None

class PdfParams(BaseModel):
    content:str = Field(...,description="pdf内容")

@tool(args_schema=PdfParams)
def pdf_tool(content:str)->str:
    """
    pdf写入
    """
    try:
        # 1.创建pdf对象 默认a4大小
        pdf = FPDF()
        pdf.add_page()

        # 2.设置字体和大小
        font_path = find_chinese_font()
        pdf.add_font("ChineseFont", fname=font_path)
        pdf.set_font("ChineseFont", size=18)

        # 3.写入一段文字
        pdf.multi_cell(0,15,content)
        file_name = time.strftime("%Y%m%d%H%M%S",time.localtime())

        # 5.保存pdf文件
        pdf.output(f"{file_name}.pdf")
        return "pdf文件写入成功"
    except Exception as e:
        print(f"出现异常{e}")
        return "pdf文件写入失败"

