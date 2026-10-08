from utils.LoadNeo4jUtil import get_neo4j_conn

conn = get_neo4j_conn()

data={
    "name":"wangwu",
    "age":18
}

#占位符$
cql="""
    CREATE (n:Person {name:$name,age:$age})

"""

cql1="""
    MATCH (n) return n
"""
a = conn.run(cql,data)  #占位符参数与实际传入的参数名要保持一致
print(a)

b = conn.run(cql1)
print(b)