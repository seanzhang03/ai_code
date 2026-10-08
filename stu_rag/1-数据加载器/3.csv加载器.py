from langchain_community.document_loaders import CSVLoader
import os
from pathlib import Path 
from langchain_core.documents import Document   

#设置文件读取路径
file_path = os.path.join(Path(os.path.dirname(__file__)).parent,"example.csv")
# file_path = os.path.join(Path(os.path.dirname(__file__)).parent,"datasets","法律数据集.csv")

#创建加载器对象并且读取数据
csv_loader=CSVLoader(file_path=file_path,encoding="utf-8")
result = csv_loader.load()
print(result)

import pandas as pd
result = pd.read_csv(filepath_or_buffer=file_path)
print(result)
print(type(result)) #DataFrame是pandas中的数据类型之一

result_list = result['城市'].to_list()
print(result_list)
data_list = []

#处理数据
for item in result_list:
    data_list.append(
        Document(page_content=item,metadata={"source":file_path})
    )
print(data_list)