from langchain_chroma import Chroma
from utils.LoadEmbeddingModel import load_embedding_model
#向量数据库连接
vector = Chroma(
    collection_name = "law",
    persist_directory=r"E:\ai_code\chroma_data\law_data",
    embedding_function=load_embedding_model(),
    collection_metadata={"hnsw:space":"cosine"}
)
#获取所有的docs
all_data = vector.get()
ids = all_data["ids"]
documents = all_data["documents"]
metadatas = all_data["metadatas"]

#处理数据的格式为List[Document]
from langchain_core.documents import Document
bm25_docs = [Document(id=ids[index],page_content=documents[index],metadata=metadatas[index]) for index in range(len(ids))]

#构建向量检索器
vector_retriever = vector.as_retriever(search_kwargs={"k":10})
#构建BM25检索器
from langchain_community.retrievers import BM25Retriever
bm25_retriever = BM25Retriever.from_documents(
    documents=bm25_docs,  #文档
    k=10, #返回的文档数量
)

#混合检索器
from langchain_classic.retrievers import EnsembleRetriever
ensemble_retriever = EnsembleRetriever(
    #检索器列表
    retrievers=[vector_retriever,bm25_retriever],
    #权重列表
    weights=[0.5,0.5]
)

#执行检索
rs = ensemble_retriever.invoke("食品安全法有哪些规定")
for index,item in enumerate(rs,start=1):
    print(f"结果{index}:{item.page_content}")


