#输出解析器
import json
from langchain_core.output_parsers import StrOutputParser

#导入向量数据库
from common.LoadChromaConn import LoadChromaConn

#提示词
from langchain_core.prompts import PromptTemplate

#构造链的工具
from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda

#重排序模型
from common.LoadRerankerModel import LoadRerankerModel
from chat.utils.RerankerUtil import reranker_util

#打印工具
from chat.utils.PrintLogUtil import print_log

#大模型
from common.LoadLLMModel import LoadLLMModel

#意图识别
from chat.utils.IntentRecognitionUtil import intent_recognition

#查询某个窗口的对话记录信息
from history.dao import  HistoryDao


#聊天
def chat(question:str,historyId:int):
    # 大模型对象
    llm = LoadLLMModel().llm
    '''
    基于historyId获取到当前对话记录信息
    关于历史记录的优化策略：
    为什么要优化：上下文窗口是有限制的，目前比较主流的qwen3.8、deepseek v4pro都是1M
    策略：1、限制对话次数策略：对话记录数做限制[对话窗口的对话次数到一定数量后，不添加新的对话记录]
        2、截取对话记录，窗口滑动：只把近几轮的对话记录信息找出来作为历史记录上下文
        滑动窗口就是消息的截取，截取近期对话信息，前期的对话信息忽略掉
        3、总结摘要：把早期对话记录进行总结，生成一个摘要信息，作为当前对话的上下文信息[防止语义丢失会完整保留近几轮+之前的摘要]
        摘要信息持久化：单独创建一张表，来存放摘要信息，这个摘要信息要保存的内容为：当前对话窗口早期对话记录，摘要需要被表示为哪个对话窗口的信息，用user_id+history_id合并标识
        摘要信息我们多少轮次进行一次摘要：假设每5轮进行一次摘要处理，最后送入模型作为上下文内容
        4、使用向量数据库：语义信息提取[只找到历史记录对话中和本轮问题相关的信息，不相关的不要]
        就是基于当前的问题去向量数据库中查询相关的当前用户的当前窗口的记录，余弦相似度进行语义匹配
        问题：指代词问题，需要处理后再去做语义匹配，否则找不到对应的值
    '''
    history_data = HistoryDao.query_history_list(historyId)
    history_list = []
    for item in history_data:
        history_list.append(
            {"role":"user","content":item["question"]}
        )
        history_list.append(
            {"role":"assistant","content":item["answer"]}
        )

    '''
    项目任务：这里应该有一个question改写操作，基于对话记录[上一条QA，可以在前面的查询出来的数据中截取]改写question中的指代词
    '''
    #添加一个意图识别的操作：目的区分当前问题是否需要走RAG检索然后回答
    is_legal = intent_recognition(question)
    #法律不相关
    if not is_legal:
        # 加载大模型的对象
        prompt = f"""
            你是一个专业的助手。请严格依据以下两部分信息回答用户当前问题：
                    1. 你自身的内部知识；
                    2. 下方提供的【历史对话记录】中的完整上下文。
                    若以上两者均无法支撑回答，请直接回复“无法回答”，禁止检索、编造或添加任何额外解释。
                    【历史对话记录】
                    {history_list}
                    【当前问题】
                    {question}
                    注意：回答时必须结合【历史对话记录】中的上下文理解当前问题的指代、省略或延续意图，不得忽略历史信息。
            """
        for chunk in llm.stream(prompt):  #流式把prompt发给大模型，stream返回的是生成器，每次yield大模型生成的一小段文本(一个chunk)
            if chunk.content:  #chunk是LangChain返回的AIMessageChunk对象，.content是实际携带的那一小段文字
                yield chunk.content

    #法律相关
    else:
        # 向量数据库连接对象
        vector = LoadChromaConn().conn
        # 重排序模型对象
        reranker_model = LoadRerankerModel().load_reranker_model()
        # 提示词
        qa_prompt = """
               你是一个基于知识库的AI助手。请根据RAG检索内容回答用户问题。
            规则：
                - 仅基于提供的知识回答，不使用外部知识补充。
                - 检索内容不足时，说明信息不足，不要猜测。
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
        prompt = PromptTemplate(template=qa_prompt, input_variables=["history","context", "question"]) #将含占位符的字符串包装成可复用的模板对象，然后可以.invoke填入具体的值，context和question就是待填充的洞

        # 重排序
        def reranker_util(docs):
            #打印召回的结果
            print_log(title="召回的结果",docs=docs)
            # 构造qa对
            data = []
            for doc in docs:
                data.append(
                    (question, doc.page_content)
                )
            reranker_scores = reranker_model.compute_score(data)
            # 分数排序
            index_docs = [i for i in range(len(reranker_scores))]  # 重排序分数的一个索引，每一个分数对应按照顺序排列的索引
            reranker_docs = [docs[i] for i in sorted(index_docs, key=lambda x: reranker_scores[x], reverse=True)][:3]  # 按顺序排索引，比如一共10个数，最大的索引为5，然后8类似这种，再通过索引交换文档顺序，来实现重排序
            print_log(title="重排序的结果", docs=reranker_docs)
            return reranker_docs

        # 构造qa链
        qa_chain = (
                RunnableParallel({  # 并行计算，这里将两个值给到context和question
                    "history":RunnableLambda(lambda _: history_list),
                    #检索器原理：将question也变为向量，计算其和库里的所有文档向量的余弦相似度，返回最相似的10条
                    "context": vector.as_retriever(search_kwargs={"k": 10}) | RunnableLambda(reranker_util),
                    # 基于检索器检索文档作为context的值
                    "question": RunnablePassthrough()  # 传递问题作为question的值 --- 透明传递
                })
                | prompt  #将RunnabbleParallel并行计算的值传递给prompt，PromptTemplate自动把{context}、{question}替换成实际内容
                | llm  #最后交给大模型和字符输出解析器
                | StrOutputParser()
        )
        # 执行
        for chunk in qa_chain.stream(question):
            if chunk:
                yield chunk


if __name__ == "__main__":
    for chunk in chat("发生家庭暴力怎么办",6):
        print(chunk)



#意图识别：区分用户的问题，实现回答任务分流
#1.和自己的知识库数据相关的内容走RAG链路
#2.和自己的知识库不相关的内容走非RAG链路

#多轮对话：用户在执行当前对话的时候，可以把之前的当前窗口的对话信息一并发送给模型，作为模型的上下文，多轮对话的实现需要历史记录
#也就是我们所说的会话记忆，属于短期记忆

