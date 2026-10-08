'''
    意图识别
'''
import json

from common.LoadOllamaModel import LoadOllamaModel
def intent_recognition(question):
    #加载ollama模型对象
    ollama_model = LoadOllamaModel().ollama_model
    #提示词
    prompt="""
    你是一个专业的电影领域意图识别专家。你的任务是判断用户的输入是否包含【电影相关】内容。

        # Definition: 什么是"电影相关"
        包括但不限于以下范畴：
        1. 电影信息查询（电影名称、导演、主演、类型、制片国家/地区、语言、上映日期、片长、豆瓣评分等）
        2. 电影推荐（根据类型、导演、主演、国家/地区、评分等条件推荐电影）
        3. 电影评价与讨论（剧情分析、角色解读、评分讨论、观影感受等）
        4. 电影对比（多部电影之间的比较，如评分、类型、导演风格等）
        5. 电影筛选与排名（按豆瓣评分排序、按类型筛选、按国家/地区筛选等）
        6. 电影人物相关（导演作品盘点、演员作品盘点、编剧作品等）
        7. 电影剧情咨询（某部电影的剧情简介、故事梗概等）

        # Definition: 什么是"不相关"
        1. 纯电视剧/综艺/动漫讨论（非电影形式）
        2. 纯粹的情感倾诉且未提及任何电影内容
        3. 日常生活闲聊、技术问题、娱乐八卦（不涉及电影）
        4. 音乐/书籍/游戏讨论（非电影形式）
        5. 虽然涉及影视但明确属于其他领域（如摄影技术、剧本创作教学等）

        # Output Format
        仅输出一个JSON对象，不要包含任何其他解释文字：
        {
            "is_film": True/False,  #是否跟电影相关
            "confidence": "high/medium/low",  #相关置信度
        }

        # Examples
        User: "肖申克的救赎的导演是谁"
        Assistant: {"is_film": true, "confidence": "high"}

        User: "推荐几部豆瓣评分9分以上的电影"
        Assistant: {"is_film": true, "confidence": "high"}

        User: "霸王别姬和活着哪个评分更高"
        Assistant: {"is_film": true, "confidence": "high"}

        User: "今天心情好差，感觉活着没意思"
        Assistant: {"is_film": false, "confidence": "high"}

        User: "Python怎么读取Excel文件"
        Assistant: {"is_film": false, "confidence": "high"}

        User: "宫崎骏有哪些作品"
        Assistant: {"is_film": true, "confidence": "high"}

        User: "推荐几部韩国的犯罪片"
        Assistant: {"is_film": true, "confidence": "high"}

        User: "最近有什么好看的电视剧"
        Assistant: {"is_film": false, "confidence": "medium"}
    """

    #意图识别--参数：role：消息是谁说的，常见有system,user,assistant content：消息正文
    #为何要区分system和user：告诉模型扮演什么角色，如何回答，有多轮对话，会追加assistant和后续user消息，让模型记住上下文
    rs = ollama_model.invoke([
        {"role":"system","content":prompt},
        {"role":"user","content":f"请解析用户的问题：{question}"}
    ])  #rs拿到的是AIMessage对象，模型生成的文本在rs.content里，按提示词要求，rs.content是json对象
    return json.loads(rs.content)["is_film"]

if __name__ == "__main__":
    print(intent_recognition("阿凡达这部电影讲的是什么"))

