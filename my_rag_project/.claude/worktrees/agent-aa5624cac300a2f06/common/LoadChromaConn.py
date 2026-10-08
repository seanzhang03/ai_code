"""
    建立与向量数据库chroma的连接
"""
#加载包
from common.LoadEmbeddingModel import load_embedding_model
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os


load_dotenv()

class LoadChromaConn:
    def __init__(self):
        #加载向量化模型
        self.embedding_model = load_embedding_model()
        self.conn = self.load_chroma_conn()

    def load_chroma_conn(self):
        return Chroma(
            #chroma文件位置
            persist_directory=os.getenv("CHROMA_DATA_PATH"), #chroma数据库路径
            collection_name=os.getenv("COLLECTION_NAME"),  #集合名称
            embedding_function=self.embedding_model,  #选择向量化模型进行向量化
            collection_metadata={"hnsw:space":"cosine"},  #余弦相似度
        )
