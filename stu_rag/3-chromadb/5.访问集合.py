import sys
sys.path.append('/')
from utils.ChromaDBUtil import get_chromadb_conn
from pathlib import Path
import os
path_dir = os.path.join(Path(os.path.dirname(__file__)).parent,"chroma_data","test3")
vector = get_chromadb_conn(path=path_dir)
#获取所有集合，collection实际上是一个列表
collections = vector.list_collections()  #vector实际上是建立chromadb连接的返回对象，为一系列向量
print(collections)

#访问指定名称集合-存在
collection = vector.get_collection(name="collection_one")
print(collection)

#访问指定名称集合-不存在，报错chromadb.errors.NotFoundError:Collection [test2] does not exist
#collection2 = vector.get_collection(name="collection_two")
#print(collection2)

#访问指定名称集合--不存在就创建
collection3 = vector.get_or_create_collection(name="collection_two")  #get_or_create_collection() 方法的行为取决于集合是否已经存在
#如果集合不存在，ChromaDB 会使用默认的嵌入函数来创建它
print(collection3)