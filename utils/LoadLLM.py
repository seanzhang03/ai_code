import os
from langchain_openai import ChatOpenAI

def load_llm():
    return ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        #模型访问路径
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        #模型名称
        model = "qwen3.8-max-0902",
        #流式输出
        streaming = True
    )