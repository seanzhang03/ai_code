#读取数据
import  os
from pathlib import Path

#文本路径
file_path = os.path.join(Path(os.path.dirname(__file__)).parent,"datasets","法律数据集.csv")
from langchain_community.document_loaders import CSVLoader
#读取数据
loader = CSVLoader(file_path=file_path,encoding="utf-8")
data = loader.load()
#入库
from langchain_chroma import Chroma
#保存路径
chroma_data_path = os.path.join(Path(os.path.dirname(__file__)).parent,"chroma_data","law_data")
#集合名称
collection_name="law"

#向量化模型
from utils.LoadEmbeddingModel import load_embedding_model
embedding_model = load_embedding_model()

#获取对象
vector = Chroma(
    collection_name=collection_name,
    persist_directory=chroma_data_path,
    collection_metadata={"hnsw:space":"cosine"}
)

#查询部分数据
results = vector.get(where_document={"$contains":"《中华人民共和国反家庭暴力法》第二十四条规定"})
print(results)