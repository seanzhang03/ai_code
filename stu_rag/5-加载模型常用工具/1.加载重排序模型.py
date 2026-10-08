#同一个模型可以用不同的加载方式，得到结果都是模型对象，如transformers 加载和sentence-transformers 加载
from FlagEmbedding import FlagReranker

#加载重排序模型
reranker_model = FlagReranker(
    #模型选择的是bge-reranker-large
    model_name_or_path=r"",
    #使用半精度推理，速度快
    use_fp16=True
)
print(f"加载的模型:{reranker_model}")

#执行重排序分数计算
scores = reranker_model.compute_score([#计算每个句子对的分数
    ("cc老师是谁？", "华清远见成都中心设有教学部、教务部、市场部等多个部门，其中教学部根据专业方向分为AI教学部和嵌入式教学部，分别负责不同技术领域的人才培养与课程教学工作。"),
    ("cc老师是谁？", "cc老师是AI教学部的一名讲师，拥有丰富的人工智能领域教学经验，在课程讲授与项目指导过程中深受学员欢迎。"),
    ("cc老师是谁？", "zs老师是AI教学部的一名讲师，拥有丰富的人工智能领域教学经验，在课程讲授与项目指导过程中深受学员欢迎。"),
    ("cc老师是谁？", "ls老师是AI教学部的一名讲师，拥有丰富的人工智能领域教学经验，在课程讲授与项目指导过程中深受学员欢迎。"),
])  
print(f"重排序后的分数:{scores}")

#分数对应的索引 --索引用来获取原始文档
index = [i for i in range(len(scores))]
#我们要把索引index进行排序，排序规则指定为分数的大小
index.sort(key=lambda i :scores[i],reverse=True)
#取出原始文档