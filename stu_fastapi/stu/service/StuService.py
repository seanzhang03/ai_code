"""
    处理StuController接口函数的功能实现
    返回值就是结果
"""
# 聊天
def chat(question, load_model):
    """
    :param question: 用户问题
    :param load_model: 加载模型的对象
    :return: 对话结果，流式返回
    """
    # 获取大模型对象
    llm = load_model.llm
    # 使用大模型回答用户问题
    for chunk in llm.stream(question):
        if chunk.content:
            yield chunk.content
             