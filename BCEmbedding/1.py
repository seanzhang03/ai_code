from BCEmbedding import  EmbeddingModel,RerankerModel

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

embedding_model = EmbeddingModel(model_name_or_path="E:/ai_code/models/maidalun1020bce-embedding-base_v1")

#文本向量化
docs_embedding = embedding_model.encode(documents)
print(docs_embedding)

query = "input_query"
document_pairs = [[query,document] for document in documents]

reranker_model = RerankerModel(model_name_or_path = "E:/ai_code/models/maidalun1020bce-embedding-base_v1")
scores = reranker_model.compute_score