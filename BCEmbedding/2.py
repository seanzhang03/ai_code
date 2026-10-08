from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
import os
from pathlib import Path
import sys
file_path = os.path.join(Path(os.path.dirname(__file__)).parent,"datasets","法律数据集.csv")
csv_loader = CSVLoader(file_path=file_path,encoding="utf-8")
result = csv_loader.load()
print(result)

sys.path.append('E:/ai_code') 
from utils.ChromaDBUtil import get_chromadb_conn #建立连接
path_dir =os.path.join(Path(os.path.dirname(__file__)).parent,"chroma_data","law_data")
#获取连接对象
vector = get_chromadb_conn(path_dir)

#引入向量化模型
from chromadb.utils import embedding_functions
model_path = "E:/ai_code/models/bge-base-zh-v1.5"
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=model_path
)

collection_law = vector.create_collection(
    name = "law",
    embedding_function=embedding_function,
    metadata={"hnsw:space":"cosine"}
)
Chroma.from_documents

show = Chroma.get_collection(name="law")
print(show)