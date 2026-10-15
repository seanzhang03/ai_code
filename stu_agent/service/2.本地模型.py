from langchain_openai import ChatOpenAI
import os
#本地模型
model = ChatOpenAI(
    model="qwen2.5:7b",
    base_url="http://localhost:11434/v1"
)
rs = model.invoke("你好")
print(rs.content)