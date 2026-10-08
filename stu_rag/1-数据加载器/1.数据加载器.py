from langchain_community.document_loaders import TextLoader
import os
from pathlib import Path

#绝对路径
#file_path = "E:\ai_code\2.txt"
#相对路径
#file_path = "../2.txt"
#绝对路径：动态获取
#os.path.dirname用来提取给定文件路径中的目录部分（去掉最后的文件名，返回其所在父目录）
#Path()：将普通字符串转换为一个Path对象
file_path = os.path.join(Path(os.path.dirname(__file__)).parent,"2.txt")

#读取文件，加载读取的结果
#直接用文件读写
with open(file_path,"r",encoding="utf-8") as f:  #encoding和rb模式不能同时指定
    print(f.read(1))
print("==========================")

#用txt加载器
text_loader = TextLoader(file_path=file_path,encoding="utf-8")
result = text_loader.load()
print(result)