from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

class LoadChromaConn:
    def __init__(self):
        #加载向量数据库连接
        self.embedding_model = self.load_embedding_model()
        self.conn = self.load_chroma_conn()

    #加载向量化模型
    @staticmethod
    def load_embedding_model():
        return HuggingFaceEmbeddings(
            model_name=os.getenv("EMBEDDING_MODEL"),
            model_kwargs={
                "device":"cpu",
                "local_files_only":True,
            },
        )

    #加载向量数据库连接对象
    def load_chroma_conn(self):
        return Chroma(
            persist_directory=os.getenv("CHROMA_DATA_PATH"),
            collection_name=os.getenv("COLLECTION_NAME"),
            embedding_function=self.embedding_model,
            collection_metadata={"hnsw:space":"cosine"}
        )

if __name__ == "__main__":
    print(LoadChromaConn().conn)