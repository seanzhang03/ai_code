"""
对读取到的csv文件进行数据处理并存储对应的内容到数据向量库chroma中
"""
from langchain_community.document_loaders import CSVLoader
from langchain_core.documents import Document
import os
import pandas as pd
from common.LoadChromaConn import LoadChromaConn
from dotenv import load_dotenv
from common.LoadEmbeddingModel import load_embedding_model

load_dotenv()


#1.csv文件读取路径
file_path = os.path.join("E:\\ai_code\\my_rag_project\\datasets","影视数据集.csv")

#2.创建加载器并读取对象
result = pd.read_csv(filepath_or_buffer=file_path,encoding="gbk")
#3.截取重要信息
name_result = result["电影名称"].to_list()  #电影名称
director_result = result["导演"] #导演名字
actor_result = result ["主演"] #主演
type_result = result["类型"] #电影类型
country_result = result["制片国家/地区"] #制片国家
language_result = result["语言"] #语言
score_result = result["豆瓣评分"] #豆瓣评分
plot_result = result["剧情简介"] #剧情简介

#4.进行拼接
name_list = ["电影名称："+item + "," for item in name_result]  #电影名称
director_list = ["导演名称："+item + "," for item in director_result]
actor_list = ["主演名称："+str(item) + "," for item in actor_result]
type_list = ["电影类型："+item + "," for item in type_result+","]
country_list = ["制片国家/地区:"+item + "," for item in country_result]
language_list = ["电影语言："+item + "," for item in language_result]
score_list = ["电影评分："+str(item) + "," for item in score_result]
plot_list = ["电影剧情简介："+item + "。"for item in plot_result]

#5.处理数据
data_list = []
for i in range(len(name_result)):
    data_list.append(
        Document(page_content=name_list[i]+director_list[i]+actor_list[i]+type_list[i]+country_list[i]+language_list[i]+score_list[i]+plot_list[i],metadata={"source":file_path})
    )

vector = LoadChromaConn().conn
results =vector.get()

#6.存入数据
try:
    vector.from_documents(
        documents=data_list,
        collection_name= os.getenv("COLLECTION_NAME"),
        persist_directory= os.getenv("CHROMA_DATA_PATH"),
        embedding=load_embedding_model(),
        collection_metadata={"hnsw:space":"cosine"}
    )
    print("数据存入成功")
except Exception as e:
    print(e)
    print("数据存入失败")

# #尝试查询部分数据
# rs = vector.get(where_document={"$contains":"千与千寻"})
# print(rs)