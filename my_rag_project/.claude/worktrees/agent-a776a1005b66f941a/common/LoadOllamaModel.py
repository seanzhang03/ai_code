'''
    加载ollama模型对象
'''
import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

class LoadOllamaModel:
    def __init__(self):
        self.ollama_model = self.load_ollama_model()
    @staticmethod
    def load_ollama_model():
        return ChatOllama(
            base_url= os.getenv("OLLAMA_BASE_URL"),
            model=os.getenv("OLLAMA_MODEL_NAME")
        )

if __name__ =="__main__":
    a = LoadOllamaModel().ollama_model
    print(a)