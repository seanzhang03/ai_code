#langchain封装了操作neo4j的库
#安装pip install langchain-neo4j
from langchain_neo4j import Neo4jGraph

#连接
graph = Neo4jGraph(
    url="neo4j://127.0.0.1:7687",
    username="neo4j",
    password="rootroot",
    database="test"
)

#编写cql查询语句，查询全部数据
cql="""
    MATCH(n) return n
"""

#执行
results = graph.query(cql)
print(results)