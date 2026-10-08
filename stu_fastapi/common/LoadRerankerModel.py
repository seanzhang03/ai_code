import os
from FlagEmbedding import FlagReranker
from dotenv import load_dotenv
load_dotenv()

class  LoadRerankerModel:
    def __init__(self):
        self.reranker_model = self.load_reranker_model()

    @staticmethod
    def load_reranker_model():
        return FlagReranker(
            model_name_or_path=os.getenv("RERANKER_MODEL"),
            use_fp16=True
        )

if __name__ == "__main__":
    a = LoadRerankerModel().reranker_model
    print(a)