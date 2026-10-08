from sentence_transformers import SentenceTransformer

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

#加载模型
embedding_model = SentenceTransformer(
    #模型名称或者模型路径
    model_name_or_path=r"/models/bge-base-zh-v1.5",
)

question = "什么是rag？"
#文本向量化--normalize_embeddings：归一化，向量的结果压缩在1内
docs_embeddings = embedding_model.encode(documents,normalize_embeddings=True)
#问题向量化
question_embedding =embedding_model.encode(question,normalize_embeddings=True)
#计算
result = [question_embedding @ doc_embedding.T for doc_embedding in docs_embeddings]
print(result)