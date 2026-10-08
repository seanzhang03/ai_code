collection_name = "hqyj"
persist_directory = "../chroma_data/test4"
# 加载向量模型
from utils.LoadEmbeddingModel import load_embedding_model

embedding_model = load_embedding_model()

# llm
from utils.LoadLLM import load_llm

llm = load_llm()

# 向量数据库对象 ---> 构造成检索器
from langchain_chroma import Chroma

# 向量数据库对象
vector = Chroma(
    collection_name=collection_name,
    persist_directory=persist_directory,
    embedding_function=embedding_model
)
# 创建检索器 --- 提供给langchain链，他会自动检索内容
vector_retriever = vector.as_retriever(search_kwargs={"k": 4})
"""
    思考代码应该如何实现这个QA流程：
    用户输入问题 ---> 向量模型生成问题向量 ---> 
    向量数据库查询相似向量 ---> 获取相似向量对应的文档【添加打印】 ---> 
    替换提示词的内容 ---> 把提示词送入LLM ---> 生成答案
"""
# 定义提示词
from langchain_core.prompts import PromptTemplate

# 提示词中的context和question仅仅是一个占位符，后面一定要赋值
qa_prompt = """
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
    【用户问题】
    {question}
"""
# 创建提示词对象
prompt = PromptTemplate(
    template=qa_prompt,  # 提示词模板
    input_variables=["context", "question"],  # 提示词里面的参数
)

# 把所有的模块，像搭积木一样搭起来【构造langchain链】
# | ---> 表示管道运算符，上一个模块的输入是下一个模块的输入
# 要求每一个模块实现 runnable，如果未实现就不可以搭建
# RunnableParallel并行执行器：一同执行
# RunnablePassthrough透明传递：不做任何的更改，直接往后面传参
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
# 打印检索结果的函数
def print_docs(docs):
    print(f"检索到的文档：")
    for index, doc in enumerate(docs, start=1):
        print(f"第{index}个文档：{doc.page_content}")
    # 打印完成后返回结果
    return docs
# 打印重排序结果的函数
def print_reranker_docs(docs):
    print(f"重排序后的文档：")
    for index, doc in enumerate(docs['context'], start=1):
        print(f"第{index}个文档：{doc.page_content}")
    # 打印完成后返回结果
    return docs


# 加载重排序模型加载类
from FlagEmbedding import FlagReranker

# 加载重排序模型
reranker_model = FlagReranker(
    # 模型选择的是：bge-reranker-large
    model_name_or_path=r'G:\models\bge-reranker-large',
    # 使用半精度推理，速度快
    use_fp16=True
)

# 重排序函数
def reranker_func(docs):
    print("开始重排序操作：")
    # 取出问题和文档
    question = docs["question"]
    context = docs["context"]
    # 定义一个列表，来存储question、文档
    reranker_data = []
    for doc in context:
        reranker_data.append(
            (question, doc.page_content)
        )
    # 计算分数
    scores = reranker_model.compute_score(reranker_data)
    # 排序
    index = [i for i in range(len(scores))]
    index.sort(key=lambda i: scores[i], reverse=True)
    # 筛选top=k个最好的文档
    reranker_docs = [context[i] for i in index[:2]]
    # 返回数据
    return {
        "context": reranker_docs,
        "question": question
    }

# 构造QA链，把所有模块串联起来
qa_chain = (
    RunnableParallel(   # 并行执行器，一同执行
        {
            "context": vector_retriever | RunnableLambda(print_docs),  # 检索器检索到的内容作为context的值，它会自动执行检索返回结果操作
            "question": RunnablePassthrough(),  # 透明传递问题，即不做任何更改，直接传递给下一个模块
        }
    )
    | RunnableLambda(reranker_func) | RunnableLambda(print_reranker_docs)    # 重排序
    | prompt  # 把第一个模块的结果作为prompt的输入，即把检索到的文档和问题一同送入提示词，生成最终的提示词
    | llm  # 把提示词送入LLM，生成答案
    | StrOutputParser()  # 输出解析器，把LLM的输出结果解析成字符串
)
# 假设问题
question = "华清远见成都中心有哪些部门？"

# 测试问题
rs = qa_chain.invoke(question)
print(rs)