
#提取图片中的数据内容要做OCR识别
from pathlib import Path
import os
from langchain_community.document_loaders import UnstructuredImageLoader
import unstructured_pytesseract as ocr  
ocr.tesseract_cmd = r"E:\Tesseract-OCR\tesseract.exe"

#设置自己安装的tesseract-ocr路径
#设置图片路径
file_path = os.path.join(Path(os.path.dirname(__file__)).parent,"image1.jpeg")
#创建图片加载器对象
image_loader = UnstructuredImageLoader(
    file_path = file_path,
    mode = 'single',
    languages = ['chi_sim']
)

#加载图片数据
image_data = image_loader.load()
print(image_data)


'''
# 提取图片中的数据内容需要做OCR识别
# 使用tesseract-ocr，需要提前安装好软件，在装库
# 导入库
from pathlib import Path
import os
from langchain_community.document_loaders import UnstructuredImageLoader
import unstructured_pytesseract as ocr
# 配置自己安装的tesseract-ocr的路径\tesseract.exe
ocr.tesseract_cmd = r"E:\Tesseract-OCR\tesseract.exe"
# 设置图片的路径
file_path = os.path.join(Path(os.path.dirname(__file__)).parent,  "image2.jpeg")
# 创建图片加载器对象
image_loader = UnstructuredImageLoader(
    file_path=file_path,
    mode='single',
    languages=['chi_sim']   # 设置语言为中文，默认英文
)
# 加载图片数据
image_data = image_loader.load()
print(image_data)
'''