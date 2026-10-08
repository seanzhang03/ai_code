#步骤：所有的操作都换成langchain的api，比如存数据和读取数据
import os
import sys
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
sys.path.append('/')
#1.构建知识库
def build_knowledge_base():
    #获取文件路径
    file_path = os.path.join(Path(os.path.dirname(__file__)).parent,"datasets","华清远见.txt")
    #读取文件
    loader = TextLoader(file_path=file_path,encoding="utf-8")
    data = loader.load()  #实际就是TextLoader(file_path=file_path,encoding="utf-8").load()
    #分割
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n","\n","。","!","?"],  #切割优先级，双换行优先级最高
        chunk_size = 150,  #最大切割长度
        chunk_overlap = 0,  #相邻块的重叠字符数，0为不允许重叠
        length_function = len
    )
    docs = text_splitter.split_documents(data)

    #导入加载向量模型的类
    from langchain_huggingface import HuggingFaceEmbeddings
    #加载向量化模型-下载模型通过hf实现--下载完成后再使用
    embedding_model = HuggingFaceEmbeddings(
        model_name = r"E:/ai_code/models/bge-base-zh-v1.5",
        model_kwargs = {
            "device":"cpu", #设置通过gpu还是cpu来计算
            "local_files_only":True, #设置只使用本地文件，不联网来进行比较
        },
    )
    dir_path =  os.path.join(Path(os.path.dirname(__file__)).parent,"chroma_data","test4")
    #导入langchain封装的chromadb
    from langchain_chroma import Chroma
    #提升vector变量的作用域：
    vector = None
    #构建向量数据库对象--直接把数据入库--返回值chromadb模型对象
    try:  
        vector = Chroma.from_documents(  #chroma数据库从文本读取数据
            documents = docs,  #文本数据--List[Document]
            collection_name = "hqyj",  #集合名称
            persist_directory = dir_path,  #存储位置,注意直接用相对位置的话，相对的是终端控制台的位置，所以最好用脚本文件路径进行动态路径拼接
            collection_metadata = {"hnsw:space":"cosine"}, #指定规则为余弦相似度
            embedding = embedding_model,  #向量化模型对象
        )
        print("向量数据库构建成功")
    except Exception as e:
        print("向量数据库构建失败",e)
        return None #构建向量数据库对象失败就结束
    #查询测试
    results = vector.get()
    print(results)  #返回字典来得到集合

if __name__ == "__main__":
    build_knowledge_base()