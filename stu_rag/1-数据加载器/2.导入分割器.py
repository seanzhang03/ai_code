from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os
from pathlib import Path

#文件路径
file_path =  os.path.join(Path(os.path.dirname(__file__)).parent,"2.txt")

#读取文件
loader = TextLoader(file_path=file_path,encoding='utf-8')
data = loader.load()
print(f"数据集内容：{data}")

#构建分割器对象
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 150,
    chunk_overlap = 50 ,
    separators=["\n\n","\n","。","!","?"],  #分割符，在前面的优先级越高
    length_function=len   #计算长度的函数
)

split_data = splitter.split_documents(data)
#开始分割split_text参数str
#splitter.split_text()
print("分割后的数据为：{split_data}")
for index,doc in enumerate(split_data,start=1):
    print(f"第{index}个块:{doc.page_content}")