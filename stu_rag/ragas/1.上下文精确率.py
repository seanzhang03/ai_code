from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import ContextPrecision
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
#准备模型对象
client = AsyncOpenAI(
    api_key="sk-ws-H.PMHEYHE.9knI.MEUCIQCG2nVewXtLYOaQb-vvgDR8XaaistHqNt_jdrDqd5VSjgIgUfyI3KT7rTgkllPqyZ0QEfwTE0VXlVxc7ZT4XG9DMHY",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
llm = llm_factory("qwen3.8-max-0902", client=client)
print(llm)

#创建指标对象  上下文利用率，精确率只需要改这里的api名称即可
scorer = ContextPrecision(llm=llm)

#进行评估
result =  scorer.score(
    #用户输入问题
    user_input="埃菲尔铁塔在哪里？",
    #参考答案
    reference="埃菲尔铁塔位于巴黎。",
    #检索的上下文  不相关的文档出现在相关文档前，指标降低
    retrieved_contexts=[
        "埃菲尔铁塔位于巴黎。",
        "柏林的勃兰登堡门位于柏林。 "
    ]
)

#打印结果
print(f"Context Precision Score: {result.value}")