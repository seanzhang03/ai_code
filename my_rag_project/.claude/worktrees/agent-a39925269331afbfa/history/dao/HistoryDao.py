'''
    本模块是存储窗口对话历史记录的表的操作
'''
from common.LoadMySQLConn import LoadMySQLConn

#通过用户id来查询数据库信息
def query_history_menu_by_userid(usersId:int):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    #选取所有窗口的第一个对话作为记录，并且将users_id作为占位来对某个用户id进行信息查询
    sql = "SELECT * FROM `history` WHERE parent_id=0 AND users_id=%s;"
    cursor.execute(sql,[usersId])
    results = cursor.fetchall()
    LoadMySQLConn().close_mysql_conn(cursor,conn)
    return results

#根据一个会话的历史id来访问该对话窗口的全部上下文信息
def query_history_list_by_historyid(historyId:int):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    #ORDER BY history_id ASC即按history_id升序排列结果，从小到大，保证先出现的记录在前面
    #WHERE history_id =%s or parent_id=%s找出根记录和其下所属的子记录
    sql = "SELECT * FROM `history` WHERE (history_id =%s or parent_id=%s) ORDER BY history_id ASC"
    cursor.execute(sql,[historyId,historyId])
    results = cursor.fetchall()
    LoadMySQLConn().close_mysql_conn(cursor,conn)
    return results

#保存一个新的对话到历史记录中
def save_chat_results(userId:int,question:str,answer:str,parentId:int):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO history VALUES(NULL,%s,%s,%s,%s,now())"
        cursor.execute(sql,[
            userId,
            question,
            answer,
            parentId
        ])
        conn.commit()  #提交事务：提交了后生效，成功提交，失败则回滚
        return cursor.lastrowid #返回history_id
    except Exception as e:
        print(f"异常原因:{e}")
        conn.rollback()  #回滚
        return 0
    finally:
        LoadMySQLConn().close_mysql_conn(cursor,conn)

if __name__ =="__main__":
    r = query_history_list_by_historyid(1)
    print(r)