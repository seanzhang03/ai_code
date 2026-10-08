from langchain_community.document_loaders import CSVLoader
from pathlib import Path
import os

file_path = os.path.join(Path(os.path.dirname(__file__)),"datasets","影视数据集.csv")
#创建csv加载器对象并读取数据
csv_loader =CSVLoader(file_path=file_path,encoding="utf-8")
result = csv_loader.load()
print(result)