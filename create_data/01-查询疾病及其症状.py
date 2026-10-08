import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_neo4j import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain_neo4j import GraphCypherQAChain

# 初始化 Neo4j 连接
graph = Neo4jGraph(
    url="bolt://127.0.0.1:7687",
    username="neo4j",
    password="rootroot",
    database="neo4j"
)


# 初始化 LLM
llm = ChatOpenAI(
    model="qwen3.6-27b",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 构建 GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    allow_dangerous_requests=True,
    verbose=True,
    top_k=10,
    validate_cypher=True
)

# 问题
questions = [
    "感冒有哪些常见症状？",
    "感冒的疾病详情是什么？",
    "咳嗽症状对应哪些疾病？"
]

answers = []

for q in questions:
    result = chain.invoke({"query": q})
    answers.append(f"问题：{q}\n回答：{result['result']}")

# 用 LLM 做综合总结
prompt = PromptTemplate(
    input_variables=["answers"],
    template="""
    请将以下问答进行综合归纳，生成一段完整、连贯的中文回答：
    {answers}
    """
)

# 构建管道
summary_pipeline = (
    RunnableMap({
        "answers": RunnablePassthrough()  # 直接传入 answers
    })
    | prompt                       # 将 answers 放入模板
    | llm                          # LLM 生成文本
    | StrOutputParser()            # 输出为字符串
)

# 执行
final_summary = summary_pipeline.invoke({
    "answers": "\n\n".join(answers)
})
print("综合回答：\n", final_summary)