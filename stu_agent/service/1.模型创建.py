from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

#创建模型
model = ChatOpenAI(
    model=os.getenv("MODEL_LINE_NAME"),
    base_url=os.getenv("LINE_BASE_URL"),
    api_key=os.getenv("LINE_API_KEY")
    #temperature即温度系数，用来控制模型输出的随机性和创造性，低温度更保守，高温度更有随机性，输出创造性，不可预测
)

#对话
rs = model.invoke("你好")
print(rs.content)
print(rs)