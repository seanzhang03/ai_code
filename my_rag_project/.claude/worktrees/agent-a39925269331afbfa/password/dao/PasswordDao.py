'''
    本模块是用户进行修改密码的数据库操作
'''
from common.LoadMySQLConn import LoadMySQLConn
from common.JWTUtil import hash_password
def query_users_by_email(email):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE email=%s"
    cursor.execute(sql,[email])
    results = cursor.fetchall()
    LoadMySQLConn.close_mysql_conn(cursor,conn)
    return results

def change_password(email,new_password):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    try:
        sql = "UPDATE users SET password=%s WHERE email=%s"
        cursor.execute(sql,[hash_password(new_password),email])
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        return 0
    finally:
        LoadMySQLConn.close_mysql_conn(cursor,conn)

if __name__ == "__main__":
    a = change_password("123456@qq.com","654321")
    print(a)