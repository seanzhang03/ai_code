'''
    本模块是用来帮助管理员的数据库操作
'''
from common.LoadMySQLConn import LoadMySQLConn
from common.JWTUtil import hash_password
#根据用户名称查询用户信息
def query_users_by_nickname(name):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE nickname=%s"
    cursor.execute(sql,[name])
    results = cursor.fetchall()
    LoadMySQLConn.close_mysql_conn(cursor,conn)
    return results

#根据邮箱来查询用户信息
def query_users_by_email(email):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE email=%s"
    cursor.execute(sql,[email])
    results = cursor.fetchall()
    LoadMySQLConn.close_mysql_conn(cursor,conn)
    return results

#创建用户操作
def create_users_with_email_nickname(email:str,nickname:str):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO users VALUES(NULL,%s,%s,%s,now(),%s)"
        cursor.execute(sql,[
            email,
            hash_password("123456"),
            nickname,
            "user",
        ])
        conn.commit()
        return cursor.lastrowid  #返回创建用户的userid
    except Exception as e:
        print(e)
        conn.rollback()  #回滚事务
        return 0
    finally:
        LoadMySQLConn().close_mysql_conn(cursor,conn)



#根据用户名进行初始化密码操作，密码初始化为123456
def password_init_by_nickname(name):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    hashed_password = hash_password('123456')
    try:
        sql = "UPDATE users SET password=%s WHERE nickname=%s;"
        cursor.execute(sql,[hashed_password,name])
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        return 0
    finally:
        LoadMySQLConn.close_mysql_conn(cursor,conn)

#根据用户名删除一个用户信息
def delete_users_by_nickname(name:str):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM users WHERE nickname=%s"
        cursor.execute(sql,[name])
        conn.commit()
        return cursor.lastrowid #返回删除的用户的id
    except Exception as e:
        print(e)
        conn.rollback()
        return 0
    finally:
        LoadMySQLConn.close_mysql_conn(cursor,conn)