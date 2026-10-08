from py2neo import Graph

def get_neo4j_conn():
    return Graph(
        #连接地址
        profile="neo4j://127.0.0.1:7687",
        #账号密码---neo4j安装好后自带的名字
        auth=("neo4j","rootroot"),
        #操作库的名字
        name="neo4j",
    )

if __name__ =="__main__":
    conn =get_neo4j_conn()
    print(conn)