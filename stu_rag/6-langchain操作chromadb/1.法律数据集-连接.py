from langchain_chroma import Chroma
from utils.LoadEmbeddingModel import load_embedding_model

#构建连接
vector = Chroma(
    #集合名称   
    collection_name="hqyj",
    #存储位置
    persist_directory=r"E:\ai_code\chroma_data\test4",
    #嵌入模型
    embedding_function=load_embedding_model(),
    #余弦相似度计算
    collection_metadata={"hnsw:space":"cosine"}
)