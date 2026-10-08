import uuid
import sys

from chromadb.utils import embedding_functions
sys.path.append("/")
from utils.ChromaDBUtil import get_chromadb_conn
from langchain_community.document_loaders import TextLoader
import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

#获取文件路径
file_path = os.path.join(Path(os.path.dirname(__file__)).parent, "datasets", "华清远见.txt")
#读取文件
loader = TextLoader(file_path=file_path,encoding="utf-8")
data = loader.load()
#分割
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "！", "？"],
    chunk_size=150,
    chunk_overlap=0,
    length_function=len
)

docs = text_splitter.split_documents(data)
path_dir= os.path.join(Path(os.path.dirname(__file__)).parent,"chroma_data","test3")
#创建ChromaDB连接
vector = get_chromadb_conn(path = path_dir)
model_path = "/models/bge-base-zh-v1.5"  #模型路径
#加载模型-得到嵌入函数的格式，而非直接的模型对象
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=model_path,  #设置模型名称，直接给的存储路径就直接读取
)

#创建集合
collection = vector.get_or_create_collection(
    name="hqyj",
    embedding_function=embedding_function,
    metadata={"hnsw:space":"cosine"}
)

#添加文档,一个集合里面有多个文档内容
try:
    for item in docs:
        collection.add(
            ids= str(uuid.uuid4()),
            documents=item.page_content,  #documents是ChromaDB里的文本内容，page_content是LangChain里的文本内容
            metadatas = item.metadata    #metadatas是ChromaDB里的元数据，而metadata是LangChain里的元数据
        )
    print("添加成功")
except Exception as e:
    print(e)
    print("添加失败")

#假设查询问题
question = "cc老师是谁？"

#query方法：chromadb中提供的通过余弦相似度查询数据的方法
results = collection.query(
    #查询的问题文本
    query_texts=question,
    #返回的结果数量
    n_results=1
)
#打印结果
print(results)
#提取结果
context = results.get("documents","")[0][0]  #第一次取索引取到包含文档列表的列表，第二次索引取到这个列表的第一个字符串元素
print(context)
#获取llm对象
from utils.LoadLLM import load_llm

llm = load_llm()

#构造对话的上下文信息 -- 放在系统提示词中
system_prompt = f"""
你是一个专业的知识库问答助手。你的所有回答必须且只能基于下方【参考上下文】中提供的信息。
【核心原则】
1. 忠实原文：答案必须完全来源于【参考上下文】，严禁使用外部知识、常识或训练数据补充回答。
2. 明确拒答：若【参考上下文】中不包含回答问题所需的信息，请直接回复"根据当前参考资料，未找到相关信息"，严禁编造、推测或模糊作答。
3. 精准引用：回答中涉及的关键事实、数据或定义，需在句末标注来源片段编号，格式为 [片段n]。
4. 简洁聚焦：直接回答问题本身，不输出开场白、寒暄、总结或与问题无关的背景介绍。
5. 保持原意：不得对上下文内容进行过度解读、主观评价或情感渲染，保持客观中立。
    
【回答规范】
- 若答案跨越多个片段，需综合整理后连贯表述，并标注所有相关片段编号。
- 若上下文存在矛盾信息，优先采用更具体、更新的内容，并注明差异。
- 若问题超出上下文范围但可部分回答，仅回答可验证的部分，并明确说明剩余部分无依据。
- 代码、命令、专有名词等保持原文大小写与格式不变。
    
【参考上下文】
{context}
"""

user_prompt =f"""
请基于以上参考上下文回答以下问题：
{question}
要求：
1. 严格遵循系统提示中的核心原则
2. 每个关键信息点标注来源片段编号
3. 若无法回答，直接使用指定拒答话术
"""

messages = [
    {"role":"system","content":system_prompt},
    {"role":"user","content":user_prompt},
]

#生成回复--流式输出
for chunk in llm.stream(messages):
    if chunk.content:
        print(chunk.content)
