#查询集合中的数据内容
import sys
import os
from pathlib import Path
sys.path.append("/")
from utils.ChromaDBUtil import get_chromadb_conn
path_dir = os.path.join(Path(os.path.dirname(__file__)).parent,"chroma_data","test3")
vector = get_chromadb_conn(path=path_dir)
collection = vector.get_collection(name="collection_two")
#查看集合中的所有数据内容
#get函数：查询文档内容，如果不给条件，就查询全部数据    
#include参数：指定返回的字段，可以为embeddings，documents，metadatas，默认documents，metadatas
results = collection.get(include=["embeddings","documents","metadatas"])
print(f"集合中所有的数据内容:{results}")

#查看集合中的数据条数
count = collection.count()
print(f"集合中的数据条数：{count}")

#查询指定ids数据 6d5f4812-b45c-4675-b840-31fbdef80286
one_data = collection.get(ids="6d5f4812-b45c-4675-b840-31fbdef80286")
print(f"指定ids的数据：{one_data}")

#查询指定ids列表数据 a2cecf9e-c349-48f1-b0d1-f72b6db5749c，8f5b2360-bf03-41d6-896c-2b916d121fe3
two_data = collection.get(ids=["a2cecf9e-c349-48f1-b0d1-f72b6db5749c","8f5b2360-bf03-41d6-896c-2b916d121fe3"])
print(f"指定ids列表的数据：{two_data}")

#where：过滤metadata中的内容，查询结果输出前进行过滤
where_data = collection.get(where={"hobby":"apple"})
print(f"过滤数据：{where_data}")

#where_document：过滤的是原始文档中内容，目前只支持包含关系
where_document_data = collection.get(where_document = {"$contains":"橙子"})
print(f"过滤文档数据{where_document_data}")