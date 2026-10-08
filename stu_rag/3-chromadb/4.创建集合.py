#mysql中存储数据通过表实现，而chromadb存储数据通过集合实现
#chromadb数据库中的集合：
#1.存储数据的地方
#2.一个chromadb存储路径可以有多个集合
#3.本质上操作chromadb就是在操作集合
#任何数据库操作，只涉及4个内容：CRUD
# 导入获取chromadb连接对象的工具
import sys
import os
sys.path.append('/')  # 添加项目根目录到系统路径,一定要加，不然找不到
#为什么找不到：python的搜索路径：默认只在sys.path中列出的路径下查找模块
#sys.path包含当前脚本所在目录、PYTHON环境变量、标准库路径等
#添加路径的作用：将根目录添加到搜索路径
from utils.ChromaDBUtil import get_chromadb_conn
# 导入加载模型的类
from chromadb.utils import embedding_functions
from pathlib import Path
path_dir = os.path.join(Path(os.path.dirname(__file__)).parent,"chroma_data","test3")
# 获取连接对象
vector = get_chromadb_conn(path=path_dir)

# 创建集合
# 安装pip install huggingface-hub=0.36.2
# model_name = "thenlper/gte-base-zh"  # 模型名称
model_path = "/models/bge-base-zh-v1.5"  # 模型路径
# 加载模型 --- 得到嵌入函数的格式，不是直接的模型对象
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(  #句子转换器嵌入功能:初始化句子变换器嵌入函数
    model_name=model_path,  # 设置模型的名称 --- 如果给的是存储路径直接就读取 
)

"""
    创建集合
"""
collection = vector.create_collection(  #返回的是一个集合collection
    name="collection_one",  # 集合名称
    embedding_function=embedding_function,  # 嵌入函数
    # {"hnsw:space": "cosine"}：设置向量计算公式为余弦相似度
    metadata={"hnsw:space": "cosine"},  # 集合的元数据 --- 可以设置向量计算公式  HNSW:Hierarchical Navigable Small World 分层可导航小世界用于在大量高维向量数据中快速找到“最近邻”
)

print(collection)