import sys
sys.path.append('/')
from utils.ChromaDBUtil import get_chromadb_conn
import os
from pathlib import Path
path_dir = os.path.join(Path(os.path.dirname(__file__)).parent,"chroma_data","test3")
vector = get_chromadb_conn(path=path_dir)

#查看所有集合
collections = vector.list_collections()
print(collections)

#删除指定集合
vector.delete_collection(name="collection_two")

#查看所有集合
collections = vector.list_collections()
print(collections)