'''
    本模块是实现问答的
'''
from chat.utils.IntentRecognition import intent_recognition
from common.LoadLLM import LoadLLM
from common.LoadChromaConn import LoadChromaConn
from common.LoadRerankerModel import LoadRerankerModel
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from chat.utils.PrintLogUtil import print_log_util
from history.dao import HistoryDao
from langchain_core.output_parsers import StrOutputParser
#结合历史对话，通过调用大模型把指代/省略问句改写成可独立理解的完整问句
def rewrite_question(query:str, history_list:list) -> str:
    if not history_list:      #无历史（第一轮）无需改写,将直接返回
        return query
    llm = LoadLLM().llm
    rewrite_prompt = f"""
    你是一个对话问题改写助手。请结合【历史对话】，把用户的【当前问题】改写成一个不依赖上下文、可独立理解的完整问题。
    改写规则：
    - 把"这部电影 / 它 / 那个导演 / 主演"等指代词替换成历史对话中的具体名称。
    - 如果当前问题本身已完整、不依赖上下文，原样返回。
    - 只输出改写后的问题本身，不要任何解释、标点或多余文字。
【历史对话】
{history_list}
【当前问题】
{query}
"""
    return llm.invoke(rewrite_prompt).content.strip()  #strip用来取出字符串两端空白字符

def chat(question:str,historyId:int):  #若要查询到一个窗口的历史记录，这个传进来的historyId必须是根对话的historyId
    #加载大模型
    llm = LoadLLM().llm
    chat_history_list = []
    history_data = HistoryDao.query_history_list_by_historyid(historyId)
    #根据目前对话的history_id(根对话的id)来决定加载结果是否为空或者其有父对话
    #history_data是查询到的该窗口所有的对话记录
    if historyId !=0:

        # print(history_data)
        # print("------------------------")
        for item in history_data:
            chat_history_list.append(
                {"role":"user","content":item["question"]}
            )
            chat_history_list.append(
                {"role":"assistant","content":item["answer"]}
            )
    print("历史记录已经加载")
    print(chat_history_list)
    #添加意图识别操作，判断当前问题是否需要走rag
    is_film = intent_recognition(question)
    #影视不相关
    if not is_film:
        print("已经进入影视不相关")
        #给定提示词
        prompt = f"""
            你是一个专业的影视回答助手。请严格依据以下两部分信息回答用户当前问题：
                    1. 你自身的内部知识；
                    2. 下方提供的【历史对话记录】中的完整上下文。
                    若以上两者均无法支撑回答，请直接回复“无法回答”，禁止检索、编造或添加任何额外解释。
                    【历史对话记录】
                    {chat_history_list}
                    【当前问题】
                    {question}
                    注意：回答时必须结合【历史对话记录】中的上下文理解当前问题的指代、省略或延续意图，不得忽略历史信息。
            """
        for chunk in llm.stream(prompt):  #流式把prompt发给大模型，stream返回生成器，每次yield大模型生成的一小段文本即一个chunk
            if chunk.content: #chunk是LangChain返回的AIMessageChunk对象，content是其携带的一小段文本
                yield chunk.content

    #影视相关：走RAG流程：这样既能保证质量也能保证速度
    # 1.通过检索器来召回一定量数据，即粗排
    # 2.重排序：找到相似度高的文档返回，即精排
    # 3.prompt模板+llm 结合历史、资料、问题生成答案
    else:
        print("已经进入影视相关")

        #连接向量数据库
        vector = LoadChromaConn().conn
        #重排序模型
        reranker_model = LoadRerankerModel().reranker_model
        #提示词
        qa_prompt = """
        你是一个基于知识库的AI助手。请根据RAG检索内容回答用户问题。
            规则：
                - 优先基于提供的参考资料和【历史记录】回答。
                - 如果参考资料和历史记录都无法支撑回答，请说明信息不足。
                - 必须结合【历史记录】中的上下文理解当前问题的指代、省略或延续意图。
                - 优先提炼关键答案，避免冗长解释。
                - 保持回答自然、简洁、有帮助。
                - 输出结果的时候，不允许输出根据提供的参考资料这样的内容
                - 输出结果的时候，如果没有参考的上下文信息，请给出一个友好的回复信息
            历史记录：
                {history}
            参考资料：
                {context}
            问题：
                {question}
            答案：
        """
        #将含占位符的字符串包装成可复用的模板对象，然后可以.invoke填入具体的值：context和question就是带填充的洞
        prompt = PromptTemplate(template=qa_prompt,input_variables=["history","context","question"])

        # 检索前：结合历史把指代问句改写成完整独立问句
        rewritten_question = rewrite_question(question, chat_history_list)
        print("改写后的问题：", rewritten_question)

        def reranker(docs):  #传进来的是一个个Documents对象
            print("重排序已经开始.")
            #打印召回的结果
            print_log_util(title="召回结果为",docs = docs)
            #构造qa对
            data = []
            for doc in docs:
                data.append((rewritten_question,doc.page_content))
            #计算重排序的分数
            reranker_scores = reranker_model.compute_score(data)
            #分数排序
            #重排序分数的一个索引，每个分数按照顺序排列的索引,即从0到len(reranker_scores)-1
            index_docs = [i for i in range(len(reranker_scores))]
            #重排序后的文档
            reranker_docs = [docs[i] for i in sorted(index_docs,key=lambda x:reranker_scores[x],reverse=True)][:3] #按顺序排索引，比如一共10个数，最大的索引为5，然后8类似这种，再通过索引交换文档顺序，来实现重排序,取前3个结果
            print_log_util(title="重排序结果：",docs=reranker_docs)
            #返回重排序文档(前3个)
            return reranker_docs

        #构造qa链
        qa_chain = (
            RunnableParallel({
                #并行计算三个变量，这里将三个值给到context和question，history
                "history":RunnableLambda(lambda _:chat_history_list),  #RunnableLambda将python函数包装成一个Runnable对象，其作用是将自定义python函数插入到Prompt、LLM、Parser组件构成的链中
                "context":RunnableLambda(lambda _:rewritten_question) | vector.as_retriever(search_kwargs={"k":10}) | RunnableLambda(reranker),
                # 基于检索器检索文档作为context
                "question":RunnableLambda(lambda _:rewritten_question)  #传递改写后的问题作为question的值
            })
            | prompt  #将RunnableParallel并行计算的值传递给prompt(根据不同情况选择不同提示词)，PromptTemplate自动把{context}、{question}占位符替换成实际内容
            | llm  #然后将提示词交给大模型
            | StrOutputParser()  #最后将大模型结果解析为纯字符串进行输出
        )
        #执行
        print("已经开始从qa链开始返回")
        for chunk in qa_chain.stream(question):
            if chunk:
                yield chunk

if __name__ == "__main__":
    for chunk in chat("这电影是谁拍的？",1):
        print(chunk)
