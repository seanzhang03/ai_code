"""
    加载向量化模型
"""
import os

from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

#解析.env文件
load_dotenv()

def load_embedding_model():
    return HuggingFaceEmbeddings(
        #模型路径
        model_name = os.getenv("EMBEDDING_MODEL"),
        #模型参数
        model_kwargs={
            "device":"cpu",  #cpu处理
            "local_files_only":True, #仅使用本地文件
        }
    )
