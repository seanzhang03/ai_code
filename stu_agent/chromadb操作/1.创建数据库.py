import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

client = chromadb.PersistentClient(
        path=os.getenv("CHROMA_DB_URL")
    )

#EphemeralClient:内存存储
#PersistentClient:持久化到本地磁盘下
#向量数据库创建
def create_db():
    client = chromadb.PersistentClient(
        path=os.getenv("CHROMA_DB_URL")
    )
    print("创建成功")

#创建集合
def create_collection():
    #获取或创建集合
    data = client.get_or_create_collection("my_collection")
    print(f"集合创建成功:{data.count()}")

#添加数据
def add_data():
    #数据源
    doucments = [
    "高血压是一种常见的慢性病，主要症状包括头痛、眩晕、耳鸣等。",
    "糖尿病患者应注意控制饮食，定期监测血糖，适量运动。",
    "高血压患者建议低盐饮食，每天食盐摄入量不超过6克。",
    "冠心病的典型症状是胸痛、胸闷，尤其在劳累后加重。"
    ]
    data = client.get_or_create_collection("my_collection")
    #添加数据
    data.add(
        documents=doucments, #指向数据集源
        #文档索引
        ids=[f"doc_{i}" for i in range(len(doucments))],  #转换为字符串
        metadatas=[  #源数据
            {"source": "华西医院", "type": "高血压"},
            {"source": "华西医院", "type": "糖尿病"},
            {"source": "华西医院", "type": "高血压"},
            {"source": "华西医院", "type": "冠心病"}]
    )
    print(f"集合长度:{data.count()}")

#查询数据
def query_data():
    data = client.get_or_create_collection("my_collection")
    rs = data.query(
        query_texts=["高血压"], #文本内容
        n_results=3
    )
    print(rs)
    new_data = []
    #文档数据
    new_data.append(rs["documents"][0])
    #欧氏距离
    distance = rs["distances"][0]
    print(distance)
    print(new_data)

#查询数据，通过字典查询
def query_data1():
    data = client.get_or_create_collection("my_collection")
    rs = data.query(
        query_texts=["糖尿病患者有什么症状"],  #必选项
        where={"type":"糖尿病"},
        n_results=2
    )
    print(rs)
    new_data = []
    #文档数据
    new_data.append(rs["documents"][0])
    #欧氏距离
    distance = rs["distances"][0]
    print(distance)
    print(new_data)

def delete_data():
    data = client.get_or_create_collection("my_collection")
    # #根据索引来删除
    # data.delete(ids=["doc_0"])
    # print(f"删除成功，现在的数据长度：{data.count()}")
    #根据元数据删除
    data.delete(where={"type":"高血压"})
    print(f"删除成功，现在的数据长度：{data.count()}")


if __name__ == '__main__':
    # create_db()
    # create_collection()
    #add_data()
    query_data()
    #query_data1()
    #delete_data()