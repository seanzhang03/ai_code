'''
    加载大模型
'''
from dotenv import load_dotenv

load_dotenv()

import os
from langchain_openai import ChatOpenAI
class LoadLLM:
    def __init__(self):
        self.llm = self.load_llm()

    @staticmethod
    def load_llm():
        return ChatOpenAI(
            api_key=os.getenv("OPEN_API_KEY"),
            base_url =os.getenv("LLM_BASE_URL"),
            model =os.getenv("LLM_NAME"),
            streaming = True,
        )
