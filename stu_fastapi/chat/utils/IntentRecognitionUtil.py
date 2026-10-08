#用于分析用户的问题，输出结果
import json

from common.LoadOllamaModel import LoadOllamaModel

def intent_recognition(question):
    #得到ollama的模型对象
    ollama_model =  LoadOllamaModel().ollama_model
    #提示词
    prompt="""
    你是一个专业的法律领域意图识别专家。你的任务是判断用户的输入是否包含【法律相关】内容。

        # Definition: 什么是"法律相关"
        包括但不限于以下范畴：
        1. 法律法规咨询（刑法、民法、劳动法、婚姻法、知识产权等）
        2. 合同纠纷、违约责任、债务追讨
        3. 诉讼、仲裁、行政复议、报案流程
        4. 律师咨询、法律援助、公证遗嘱
        5. 交通事故/工伤/医疗事故的赔偿责任认定
        6. 消费者权益保护、维权投诉
        7. 公司合规、股权架构、破产清算

        # Definition: 什么是"不相关"
        1. 纯情感倾诉且未提及任何权益/纠纷/规则
        2. 纯粹的道德伦理讨论（不涉及法律评价）
        3. 日常生活闲聊、技术问题、娱乐八卦
        4. 虽然涉及冲突但明确属于私人恩怨且无法律诉求

        # Output Format
        仅输出一个JSON对象，不要包含任何其他解释文字：
        {
            "is_legal": True/False,  #是否跟法律相关
            "confidence": "high/medium/low",  #相关置信度
        }

        # Examples
        User: "我和房东签了合同但他不退押金怎么办"
        Assistant: {"is_legal": true, "confidence": "high"}

        User: "今天心情好差，感觉活着没意思"
        Assistant: {"is_legal": false, "confidence": "high"}

        User: "Python怎么读取Excel文件"
        Assistant: {"is_legal": false, "confidence": "high"}

        User: "邻居半夜唱歌太吵了"
        Assistant: {"is_legal": true, "confidence": "medium"}

    """

    #意图识别
    rs = ollama_model.invoke([  #langchain中用于同步调用本地Ollama大语言模型进行推理的核心方法，将构建的提示词或消息队列喂给invoke，和本地ollama服务通信
        {"role":"system","content":prompt},
        {"role":"user","content":f"请解析用户的问题:{question}"}
    ])
    return json.loads(rs.content)["is_legal"]

if __name__== "__main__":
    if json.loads(intent_recognition("hello"))["is_legal"] == "true":
        print(1)
    else:
        print(2)
    print(intent_recognition("hello"))
    print(intent_recognition("发生家庭暴力怎么办"))
    print(intent_recognition("今天天气怎么样"))
