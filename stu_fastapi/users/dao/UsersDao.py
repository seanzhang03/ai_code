#该文件是用来针对于用户模块操作数据库的代码实现

from common.LoadDatabaseConn import LoadDatabaseConn

#根据用户邮箱查询用户信息，这里的邮箱是收件人信息
def query_users_by_email(email):
    conn = LoadDatabaseConn().load_mysql_conn()
    cursor = conn.cursor()
    sql = "select * from users where email=%s;"
    cursor.execute(sql,[email])
    results = cursor.fetchall()
    LoadDatabaseConn.close_mysql_conn(cursor,conn)
    return results

