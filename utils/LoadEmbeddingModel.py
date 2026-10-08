from langchain_huggingface import HuggingFaceEmbeddings

def load_embedding_model():
    return  HuggingFaceEmbeddings(
        model_name=r"E:/ai_code/models/bge-base-zh-v1.5",
        model_kwargs={
            "device":"cpu",
            "local_files_only":True,
        },
    )