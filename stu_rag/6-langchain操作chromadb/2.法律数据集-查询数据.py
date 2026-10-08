from utils.LangChainChromaUtil import get_chroma_conn

vector = get_chroma_conn()

#查询全部数据
results = vector.get()
print(results)

#查询原文档包含cc的内容
results1 = vector.get(where_document={"$contains":"cc"})
print(results1)