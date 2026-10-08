#FlagEmbedding加载向量化模型：可在huggingface、modelscope找到模型的使用案例
from FlagEmbedding import FlagModel

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
    #模型名称或存储位置
    model_name_or_path=r"/models/bge-base-zh-v1.5",
    query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：", #查询指令
    use_fp16= True #使用半精度推理
)

#文本向量化--等价于向量数据库里的数据存储
docs_embeddings = embedding_model.encode(documents)
#准备问题
question = "苹果公司最新消息是什么"
#问题向量化
question_embedding = embedding_model.encode([question])
#通过余弦相似度计算相似度---使用问题和每一个文本向量做计算
results = [score[0] for score in [question_embedding @ doc_embedding.T for doc_embedding in docs_embeddings]]
print(results)