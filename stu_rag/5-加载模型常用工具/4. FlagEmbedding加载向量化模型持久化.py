# FlagEmbedding加载向量化模型：可以在huggingface、modelscope找到模型的使用案例
from FlagEmbedding import FlagModel
import numpy as np

#保存文档向量化结果和原始文档数据--持久化操作
def save_docs():
    #准备测试数据
    documents = [
        "FlagEmbedding 是一个由北京智源人工智能研究院开发的文本嵌入模型。",
        "它可以将文本转换为高维向量，用于计算语义相似度。",
        "BGE 模型在 Massive Text Embedding Benchmark (MTEB) 排行榜上取得了优异的成绩。",
        "RAG（检索增强生成）是一种利用外部知识库来增强大模型回答能力的技术。",
        "苹果公司由史蒂夫·乔布斯、史蒂夫·沃兹尼亚克和罗恩·韦恩于 1976 年创立。",
        "苹果最新款的智能手机是 iPhone 15系列，搭载了A17 Pro芯片。",
        "熊猫是中国的国宝，主要栖息地是四川、陕西和甘肃的山区。",
        "深度学习是机器学习的一个分支，它基于深层神经网络。"
    ]
    #加载向量化模型
    embedding_model = FlagModel(
        #模型名称或模型存储位置
        model_name_or_path=r"/models/bge-base-zh-v1.5",
        query_instruction_for_retrieval = "为这个句子生成表示以用于检索相关文章：", #查询指令
        use_fp16=True  #是否使用半精度推理
    )
    #文本向量化--等价于向量数据库中的数据存储
    docs_embeddings = embedding_model.encode(documents)
    #savez:把数据按照数组的格式保存在文件中
    #参数
    #1、file：保存后的文件名
    #2、docs_embeddings：保存文档向量化结果[属性名任取]
    #3、documents：保存原始文档数据[属性名任取]

    np.savez(
        file=r"/datasets/test.npz",
        docs_embeddings = docs_embeddings,
        documents = documents
    )

#取出保存的文档向量化结果和原始文档数据
def load_docs():
    #np.load方法：加载通过np.savez保存的文件
    data = np.load(r"/datasets/test.npz")
    #通过存入数据的时候设置的key取出对应的值docs_embeddings,documents
    docs_embeddings = data["docs_embeddings"]
    documents = data["documents"]
    print(docs_embeddings)
    print(documents)

if __name__ == "__main__":
    #save_docs()
    load_docs()