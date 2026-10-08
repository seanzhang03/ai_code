from common.LoadDatabaseConn import LoadDatabaseConn

conn = LoadDatabaseConn().load_mysql_conn()
print(conn)
cursor = conn.cursor()

sql = "select * from users where email=%s"
cursor.execute(sql,["2012761893@qq.com"])

results = cursor.fetchall()  #fetchall是游标对象的方法，用来获取查询结果集中所有剩余行
print(results)
LoadDatabaseConn.close_mysql_conn(cursor,conn)