import sys
import os
from pathlib import Path
sys.path.append("/")
from utils.ChromaDBUtil import get_chromadb_conn
#删除文档，参数删除的ids或者where或者where_document
path_dir= os.path.join(Path(os.path.dirname(__file__)).parent,"chroma_data","test3")
vector = get_chromadb_conn(path=path_dir)
collection = vector.get_collection(name="collection_two")
try:
    collection.delete(ids="8f5b2360-bf03-41d6-896c-2b916d121fe3")
    print("删除成功")
except  Exception as e:
    print(e)
    print("删除失败")

#再次检查是否删除成功
print(collection.get())