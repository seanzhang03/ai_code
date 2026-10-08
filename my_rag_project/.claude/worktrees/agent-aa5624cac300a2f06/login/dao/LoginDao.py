'''
该模块实现针对于登录模块操作数据库的操作
'''
from common.LoadMySQLConn import LoadMySQLConn
#根据用户邮箱查询用户信息
def query_users_by_email(email):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()  #游标是执行sql语句和获取结果的核心工具
    sql = "SELECT * FROM users WHERE email=%s"  #在users表里查询where email = 所给值的所有用户信息
    cursor.execute(sql,[email])  #执行sql语句，email参数按照列表/元组形式传入
    results = cursor.fetchall()  #取出所有查询结果
    LoadMySQLConn.close_mysql_conn(cursor,conn)
    return results

#根据用户名称查询用户信息
def query_users_by_nickname(name):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE nickname=%s"
    cursor.execute(sql,[name])
    results = cursor.fetchall()
    LoadMySQLConn.close_mysql_conn(cursor,conn)
    return results

if __name__ == "__main__":
    print(query_users_by_email("2012761893@qq.com"))