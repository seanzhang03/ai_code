from langchain_community.chains.graph_qa.prompts import CYPHER_GENERATION_PROMPT, CYPHER_GENERATION_TEMPLATE
from langchain_neo4j import Neo4jGraph
from utils.LoadLLM import load_llm

#langchain提供的知识图谱问答链
from langchain_neo4j import GraphCypherQAChain
from langchain_core.prompts import PromptTemplate

#自己写的问答
def chat(question:str):
    #连接
    graph = Neo4jGraph(
        url="neo4j://127.0.0.1:7687",
        username="neo4j",
        password="rootroot",
        database="neo4j",
    )
    #利用大模型将question转为cypher语句：
    #1.先用大模型抽取出来三元组，除了大模型外，有一个开源项目PP-UIE专门做这个的
    #2.把三元组转为cypher语句

    #基于自己数据库的情况来构造提示词
    prompt='''
    如果涉及疾病、症状、药物、检查、科室、食物等医疗知识查询，调用此工具查询 neo4j 图数据库。
    只查询用户问题直接相关的内容，不要添加无关信息。

    ==================================================
    数据库 Schema
    ==================================================

    【核心节点：Disease（疾病）】
    属性名 → 中文含义对照表（查询时严格按此映射选择字段）：

    | 属性名          | 中文含义     | 用户可能的问法                   |
    |----------------|-------------|--------------------------------|
    | name           | 疾病名称     | "XX是什么病"、"介绍一下XX"       |
    | cause          | 病因         | "XX是什么原因引起的"、"XX的病因"  |
    | desc           | 疾病描述     | "介绍一下XX"、"XX是什么"         |
    | prevent        | 预防措施     | "怎么预防XX"、"XX如何预防"       |
    | get_way        | 传播途径     | "XX怎么传播的"、"XX会传染吗"     |
    | get_prob       | 发病率       | "XX的发病率高吗"、"得XX的概率"   |
    | cured_prob     | 治愈率       | "XX能治好吗"、"XX的治愈率"       |
    | cure_lasttime  | 治疗周期     | "XX要治多久"、"XX治疗需要多长时间"|
    | cost_money     | 治疗费用     | "治XX要花多少钱"、"XX的治疗费用"  |
    | yibao_status   | 医保状态     | "XX能走医保吗"、"XX医保报销吗"   |

    【其他节点】（均只有 name 属性，用于关系查询）：
    | 节点标签       | 中文含义   | 数量    |
    |---------------|-----------|--------|
    | Category      | 疾病分类   | 55     |
    | Department    | 就诊科室   | 54     |
    | Symptom       | 症状       | 5998   |
    | Cureway       | 治疗方式   | 544    |
    | Check         | 检查项目   | 3353   |
    | Drug          | 药物       | 3828   |
    | Food          | 食物       | 366    |
    | Dishes        | 菜肴       | 4506   |

    【关系类型对照表】
    | 关系名                 | 中文含义       | 起点→终点        |
    |-----------------------|---------------|-----------------|
    | DISEASE_SYMPTOM       | 疾病症状       | Disease→Symptom |
    | DISEASE_ACOMPANY      | 并发/伴随疾病  | Disease→Disease |
    | DISEASE_DEPARTMENT    | 就诊科室       | Disease→Department |
    | DISEASE_CUREWAY       | 治疗方式       | Disease→Cureway |
    | DISEASE_CHECK         | 检查项目       | Disease→Check   |
    | DISEASE_DRUG          | 治疗药物       | Disease→Drug    |
    | DISEASE_DO_EAT        | 推荐食物       | Disease→Food    |
    | DISEASE_NOT_EAT       | 忌食食物       | Disease→Food    |
    | DISEASE_DISHES        | 适合菜肴       | Disease→Dishes  |
    | DISEASE_CATEGORY      | 疾病分类       | Disease→Category |

    ==================================================
    Cypher 查询指南（按用户意图分类）
    ==================================================

    【类型A】查询疾病自身属性（病因、描述、预防、费用、治愈率、医保等）
      → 直接查 Disease 节点属性，无需关系
      用户："感冒是什么原因引起的？"
      MATCH (d:Disease {name: '感冒'}) RETURN d.cause

      用户："感冒能治好吗？治疗要花多少钱？"
      MATCH (d:Disease {name: '感冒'}) RETURN d.cured_prob, d.cost_money, d.cure_lasttime

      用户："怎么预防感冒？感冒会传染吗？"
      MATCH (d:Disease {name: '感冒'}) RETURN d.prevent, d.get_way

    【类型B】查询疾病关联的其他节点（症状/药物/科室/检查等）
      → 使用对应关系

      用户："感冒有什么症状？"
      MATCH (d:Disease {name: '感冒'})-[:DISEASE_SYMPTOM]->(s:Symptom) RETURN s.name

      用户："感冒该去哪个科室？"
      MATCH (d:Disease {name: '感冒'})-[:DISEASE_DEPARTMENT]->(dep:Department) RETURN dep.name

      用户："感冒用什么药？"
      MATCH (d:Disease {name: '感冒'})-[:DISEASE_DRUG]->(dr:Drug) RETURN dr.name

      用户："感冒需要做什么检查？"
      MATCH (d:Disease {name: '感冒'})-[:DISEASE_CHECK]->(c:Check) RETURN c.name

      用户："感冒怎么治疗？"
      MATCH (d:Disease {name: '感冒'})-[:DISEASE_CUREWAY]->(cw:Cureway) RETURN cw.name

    【类型C】查询饮食相关（推荐/忌食/菜肴）
      用户："感冒适合吃什么？"
      MATCH (d:Disease {name: '感冒'})-[:DISEASE_DO_EAT]->(f:Food) RETURN f.name

      用户："感冒不能吃什么？"
      MATCH (d:Disease {name: '感冒'})-[:DISEASE_NOT_EAT]->(f:Food) RETURN f.name

      用户："感冒适合吃什么菜？"
      MATCH (d:Disease {name: '感冒'})-[:DISEASE_DISHES]->(di:Dishes) RETURN di.name

    【类型D】查询并发/伴随疾病
      用户："感冒会引起什么并发症？"
      MATCH (d:Disease {name: '感冒'})-[:DISEASE_ACOMPANY]->(a:Disease) RETURN a.name

    【类型E】查询疾病分类
      用户："感冒属于哪一类疾病？"
      MATCH (d:Disease {name: '感冒'})-[:DISEASE_CATEGORY]->(c:Category) RETURN c.name

    【模糊匹配】疾病名称可能不完全精确时：
      - 优先用精确匹配：{name: '用户输入的名称'}
      - 精确匹配无结果时，用 CONTAINS：
        MATCH (d:Disease) WHERE d.name CONTAINS '感冒' RETURN d.name, d.cause
      - 或用正则：
        MATCH (d:Disease) WHERE d.name =~ '.*感冒.*' RETURN d.name, d.cause

    【组合查询】用户一次问多个维度时，可合并查询：
      用户："感冒的症状和用什么药？"
      MATCH (d:Disease {name: '感冒'})
      OPTIONAL MATCH (d)-[:DISEASE_SYMPTOM]->(s:Symptom)
      OPTIONAL MATCH (d)-[:DISEASE_DRUG]->(dr:Drug)
      RETURN d, collect(DISTINCT s.name) AS 症状, collect(DISTINCT dr.name) AS 药物

    【注意事项】
    - 只生成 MATCH / RETURN 类型的只读 Cypher，禁止 CREATE/DELETE/MERGE/SET 等写操作
    - 只查询用户问题中明确提到的疾病，不要自行扩展
    - 查询结果为空时，告知用户"未查询到相关数据"
    - 尽量用精确匹配，模糊匹配仅作为兜底方案
    - 只需要输出cypher语句，不要添加任何其他内容，比如```cypher和```都是不需要输出的
    '''
    #调用大模型生成cypher语句---把问题转为cql
    llm = load_llm()
    rs = llm.invoke(f"{prompt},请把{question}转为cypher语句")
    cql = rs.content
    print(cql)
    #执行生成的CQL
    result = graph.query(cql)
    #名词对齐，同样的内容用不同名词来表达
    #给大模型返回结果
    rs = llm.invoke(f"根据以下cypher语句的查询结果：{result},回答用户问题{question}")
    print(rs.content)

#langchain提供的QA链
def chat1(question:str):
    llm = load_llm()
    graph = Neo4jGraph(
        url="neo4j://127.0.0.1:7687",
        username="neo4j",
        password="rootroot",
        database="neo4j"
    )
    #生成CQL的提示词，两个参数schema、question
    CYPHER_GENERATION_TEMPLATE="""
    Task:Generate Cypher statement to query a graph database.
    Instructions:
    Use only the provided relationship types and properties in the schema.
    Do not use any other relationship types or properties that are not provided.
    Schema:
    {schema}

    # 节点标签及含义
    | 节点标签     | 含义             |
    |--------------|------------------|
    | Disease      | 疾病（核心节点） |
    | Symptom      | 症状             |
    | Check        | 检查项目         |
    | Cureway      | 治疗方式         |
    | Drug         | 药物             |
    | Department   | 就诊科室         |
    | Food         | 食物             |
    | Dishes       | 菜肴             |
    | Category     | 疾病分类         |

    # 关系类型及含义
    | 关系类型             | 含义              | 起始节点 | 目标节点    |
    |----------------------|-------------------|----------|-------------|
    | DISEASE_SYMPTOM      | 疾病症状          | Disease  | Symptom     |
    | DISEASE_CHECK        | 相关检查项目      | Disease  | Check       |
    | DISEASE_CUREWAY      | 治疗方式          | Disease  | Cureway     |
    | DISEASE_DRUG         | 治疗或相关药物    | Disease  | Drug        |
    | DISEASE_DEPARTMENT   | 就诊科室          | Disease  | Department  |
    | DISEASE_DO_EAT       | 推荐进食的食物    | Disease  | Food        |
    | DISEASE_NOT_EAT      | 不推荐进食的食物  | Disease  | Food        |
    | DISEASE_DISHES       | 适合疾病的菜肴    | Disease  | Dishes      |
    | DISEASE_ACOMPANY     | 并发症 / 伴随疾病 | Disease  | Disease     |
    | DISEASE_CATEGORY     | 疾病所属类别      | Disease  | Category    |

    # 查询示例
    # 问：高血压有哪些症状？
    MATCH (d:Disease {{name:"高血压"}})-[:DISEASE_SYMPTOM]->(s:Symptom) RETURN s.name AS symptom

    # 问：感冒吃什么药？
    MATCH (d:Disease {{name:"感冒"}})-[:DISEASE_DRUG]->(dr:Drug) RETURN dr.name AS drug

    # 问：糖尿病不宜吃什么？
    MATCH (d:Disease {{name:"糖尿病"}})-[:DISEASE_NOT_EAT]->(f:Food) RETURN f.name AS food

    # 问：肺炎需要做什么检查？
    MATCH (d:Disease {{name:"肺炎"}})-[:DISEASE_CHECK]->(c:Check) RETURN c.name AS check_item

    # 问：高血压挂什么科？
    MATCH (d:Disease {{name:"高血压"}})-[:DISEASE_DEPARTMENT]->(dep:Department) RETURN dep.name AS department

    # 问：感冒的并发症有哪些？
    MATCH (d:Disease {{name:"感冒"}})-[:DISEASE_ACOMPANY]->(a:Disease) RETURN a.name AS complication

    # 问：糖尿病属于哪类疾病？
    MATCH (d:Disease {{name:"糖尿病"}})-[:DISEASE_CATEGORY]->(c:Category) RETURN c.name AS category

    # 问：高血压可以吃什么菜？
    MATCH (d:Disease {{name:"高血压"}})-[:DISEASE_DISHES]->(dishes:Dishes) RETURN dishes.name AS dishes

    # 问：哪些疾病会有头痛症状？
    MATCH (d:Disease)-[:DISEASE_SYMPTOM]->(s:Symptom {{name:"头痛"}}) RETURN d.name AS disease

    Note: Do not include any explanations or apologies in your responses.
    Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
    Do not include any text except the generated Cypher statement.

    The question is:
    {question}"""
    # 生成回答的提示词，两个参数context、question
    QA_TEMPLATE = """你是一名专业的医疗智能问答助手，基于 Neo4j 疾病知识图谱为用户提供准确的健康咨询。

    # 第一步：意图识别
    判断用户问题是否属于【医疗疾病类】，包括但不限于：
    - 疾病症状、病因、并发症
    - 检查项目、就诊科室
    - 治疗方式、用药建议
    - 饮食宜忌、推荐菜肴
    - 疾病分类与归属

    # 第二步：按类别处理

    ## 情形 1：属于医疗疾病类 → 基于以下图谱查询结果作答
    - 严格基于查询结果作答，不得编造疾病、药物或诊疗方案
    - 若查询结果为空，回复："知识库中未收录该疾病的相关信息，建议咨询专业医生"

    ## 情形 2：不属于医疗疾病类
    - 忽略知识图谱查询结果
    - 基于自身通用知识自然作答
    - 回复中不得出现"知识库""图谱""上下文"等字样

    # 输出要求
    - 直接给出最终答案，不复述问题、不解释判断过程
    - 涉及用药、治疗、剂量等敏感内容时，附加一句："具体方案请遵医嘱"
    - 语言简洁、准确、通俗易懂

    ---
    【图谱查询结果】
    {context}

    【用户问题】
    {question}

    【回答】
    """
    #构造提示词对象
    cypher_prompt = PromptTemplate(
        template=CYPHER_GENERATION_TEMPLATE,
        input_variables=["schema","question"],
    )
    #构造问答链提示词
    qa_prompt = PromptTemplate(
        template=QA_TEMPLATE,
        input_variables=["context","question"]
    )

    qa_chain = GraphCypherQAChain.from_llm(
        #neo4j的连接对象
        graph=graph,
        #大模型对象：生成cql和生成回答用同一个模型
        llm=llm,
        #生成cypher语句的提示词
        cypher_prompt = cypher_prompt,
        #生成回答的提示词
        qa_prompt=qa_prompt,
        #允许危险请求
        allow_dangerous_requests=True
    )
    #生成回答
    rs = qa_chain.invoke({"query":question})
    print(rs)

if __name__ == "__main__":
    chat("腹泻是什么原因导致的？可以吃什么食物，不可以吃什么食物？")
