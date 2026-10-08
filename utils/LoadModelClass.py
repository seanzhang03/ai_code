from langchain_openai import ChatOpenAI
import os


class LoadModelClass:
    """
        初始化方法：目的是加载各个模型
    """

    def __init__(self):
        # 大模型
        self.llm = self.load_llm()

    # 加载大模型函数
    @staticmethod
    def load_llm():
        return ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            model="qwen3.8-max-0902",
            streaming=True,
        )
