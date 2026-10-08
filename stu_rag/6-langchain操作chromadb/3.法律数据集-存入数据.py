#结合读取 csv文件的方式，把法律数据集存入到向量数据库中
#保存在根目录/chroma_data/law_data中，集合名称law
#向量化模型
#读取数据
import pandas as pd
import os
from pathlib import Path
#文本路径
file_path = os.path.join(Path(os.path.dirname(__file__)).parent,"datasets","法律数据集.csv")

from langchain_community.document_loaders import CSVLoader
#读取数据
loader = CSVLoader(file_path=file_path,encoding="utf-8")
data1 = loader.load()
print(data1)
print("-----------------------------------------------------")
df = pd.read_csv(filepath_or_buffer=file_path,encoding="utf-8")["text"]
#df类型转list
from langchain_core.documents import Document
data = [Document(metadata = {"source":file_path},page_content=item) for item in df.tolist()] #只有metadata和page_content两个元素
# print(data)
#入库
from langchain_chroma import Chroma
#保存路径
chroma_data_path = os.path.join(Path(os.path.dirname(__file__)).parent,"chroma_data","law_data")
#集合名称
collection_name = "law"

#向量化模型
from utils.LoadEmbeddingModel import load_embedding_model
embedding_model = load_embedding_model()

#存入数据
try:
    Chroma.from_documents(
        documents=data,
        collection_name=collection_name,
        persist_directory=chroma_data_path,
        collection_metadata={"hnsw:space":"cosine"},
        embedding=embedding_model
    )
    print("操作成功")
except Exception as e:
    print(e)
    print("操作失败")