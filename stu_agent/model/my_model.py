from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

#读取配置文件
load_dotenv()


class MyModel:
    #在线大模型的私有属性
    _line_model = None
    #本地大模型的私有属性
    _local_model = None

    #在线大模型的封装
    @staticmethod
    def get_line_model():
        #第一次创建模型对象
        if MyModel._line_model is None:
            MyModel._line_model = ChatOpenAI(
                model=os.getenv("MODEL_LINE_NAME"),
                api_key=os.getenv("LINE_API_KEY"),
                base_url=os.getenv("LINE_BASE_URL"),
                streaming=True
            )
        #返回模型对象
        return MyModel._line_model

    #本地大模型的封装
    @staticmethod
    def get_local_model():
        #第一次创建模型对象
        if MyModel._local_model is None:
            MyModel._local_model = ChatOpenAI(
                model=os.getenv("MODEL_LOCAL_NAME"),
                base_url=os.getenv("LOCAL_BASE_URL"),
                streaming=True
            )
        #返回模型对象
        return MyModel._local_model

if __name__ == '__main__':
    model = MyModel.get_line_model()
    rs = model.invoke("hello")
    print(rs.content)