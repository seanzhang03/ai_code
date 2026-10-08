import jieba
from rank_bm25 import BM25Okapi

STOP_WORDS = set([
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都",
    "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会",
    "着", "没有", "看", "好", "自己", "这", "那", "他", "她", "它", "们",
    "这个", "那个", "什么", "哪", "怎么", "吗", "呢", "吧", "啊", "哦",
    "还", "被", "把", "让", "从", "对", "与", "但", "而", "或", "所",
    "为", "以", "及", "可", "可以", "能", "能够", "应该", "需要", "已经",
    "虽然", "如果", "因为", "所以", "只是", "还是", "不过", "然后",
    "之", "其", "中", "等", "等等", "即", "使", "向", "将", "按", "当",
    "于", "由", "比", "除了", "关于", "以及", "并且", "此外", "另外",
    "过", "着", "来", "去", "做", "作", "像", "如", "如同", "由于",
])

def tokenize(text):
    data=[]
    for item in list(jieba.cut(text)):
        if item in STOP_WORDS or len(item.strip())==0:
            continue
        data.append(item)
        #返回的是一个列表
    return data


from langchain_chroma import Chroma
from utils.LoadEmbeddingModel import load_embedding_model

#向量数据库连接
vector = Chroma(
    collection_name = "law",
    persist_directory=r"E:\ai_code\chroma_data\law_data",
    embedding_function=load_embedding_model(),
    collection_metadata={"hnsw:space":"cosine"}
)
#获取所有的docs
all_data = vector.get()
ids = all_data["ids"]
documents = all_data["documents"]
metadatas = all_data["metadatas"]

print(ids)
print(documents)
print(metadatas)
#处理数据的格式为List[Document]
from langchain_core.documents import Document
bm25_docs = [Document(id=ids[index],page_content=documents[index],metadata=metadatas[index]) for index in range(len(ids))]

#分词处理
tokenizer_results=[tokenize(doc) for doc in documents]
print(tokenizer_results)
#创建bm25对象
bm25 = BM25Okapi(tokenizer_results)

#准备测试用例：
question = "发生家庭暴力怎么办"
#问题分词处理
question_tokens =tokenize(question)
print(question_tokens)
#调用get_scores方法计算结果
bm25_scores =bm25.get_scores(question_tokens)
#排序筛选前10个
bm25_top10_indices = sorted(range(len(bm25_scores)),key=lambda k:bm25_scores[k],reverse=True)[:10] #降序排列
#取出数据
bm25_results_docs = [bm25_docs[index] for index in bm25_top10_indices]
print("BM25检索结果：")
for index,item in enumerate(bm25_results_docs,start=1):
    print(f"第{index}个结果：{item.page_content}")
print("-----------------------------------------------")

#向量检索
#检索器
vector_retriever = vector.as_retriever(search_kwargs={"k":10})
#执行检索
vector_results_docs = vector_retriever.invoke(question) #List[Document]
print("向量检索结果")
for index,item in enumerate(vector_results_docs,start=1):
    print(f"第{index}个结果：{item.page_content}")

#rrf融合：不考虑分值问题，只考虑排名问题--公式：rrf=求和 1/(rank+60)
rrf_scores=[]
#先处理向量检索结果，再处理BM25检索结果--结果把id作为key，rrf计算结果作为value
#核心思路：id相同，key相同，结果就相加，否则单独存入
scores_list = {} #rrf分数
docs_list = {} #文档
for index,item in enumerate(vector_results_docs,start=1):
    scores_list[item.id] = 1/(index+60) #rrf分数
    docs_list[item.id] = item #文档

for index,item in enumerate(bm25_results_docs,start=1):
    # rrf分数
    scores_list[item.id] = scores_list.get(item.id,0)+ 1/(index+60) #如果key在字典中，返回key的值，否则返回默认值
    docs_list[item.id] = item #文档

print("rrf融合检索结果：")
for index,(key,value) in enumerate(scores_list.items(),start=1):
    print(f"第{index}个结果：{docs_list[key].page_content},分数{value}")