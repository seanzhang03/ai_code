import uuid
import sys
sys.path.append('/')
from utils.ChromaDBUtil import get_chromadb_conn
import os
from pathlib import Path
path_dir = os.path.join(Path(os.path.dirname(__file__)).parent,"chroma_data","test3")
#获取连接对象
vector = get_chromadb_conn(path=path_dir)
#获取集合
collection = vector.get_collection(name="collection_two")
#准备文本
docs=[
    "小明喜欢苹果",
    "小红喜欢香蕉", 
    "小刚喜欢橙子"
]

#把文本加到test2集合中
hobby=["apple","banana","orange"]
try:
    collection.add(  #将嵌入添加到数据存储中 embeddings:要加入的embeddings，如果为“无”，则将使用为集合设置的嵌入函数基于文档或图像计算嵌入
        ids = [str(uuid.uuid4()) for _ in docs], #使用uuid随机生成的id，本质是唯一值,生成一个32位16进制字符
        documents = docs,  #文本内容
        metadatas=[{"hobby":item} for item in hobby]  #元数据
    )
    print("添加成功")
except Exception as e:
    print(e)
    print("添加失败")