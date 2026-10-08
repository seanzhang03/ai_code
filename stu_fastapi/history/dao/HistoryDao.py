#历史记录操作

from common.LoadMySQLConn import LoadMySQLConn

#查询历史记录菜单
def query_history_menu(usersId):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    sql = "SELECT * FROM `history` WHERE parent_id=0 AND users_id=%s;"
    cursor.execute(sql,[usersId])
    results = cursor.fetchall()
    LoadMySQLConn().close_mysql_conn(cursor,conn)
    return results

#根据会话id查询完整历史对话记录
def query_history_list(historyId):
    conn = LoadMySQLConn().conn
    cursor =conn.cursor()
    sql = "SELECT * FROM `history` WHERE history_id=%s or parent_id=%s ORDER BY history_id ASC"
    cursor.execute(sql,[historyId,historyId])
    results = cursor.fetchall()
    LoadMySQLConn().close_mysql_conn(cursor,conn)
    return results

#保存对话结果
def save_chat_result(saveResultEntity):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO history VALUES(NULL,%s,%s,%s,%s,now())"
        cursor.execute(sql,[
            saveResultEntity.usersId,
            saveResultEntity.question,
            saveResultEntity.answer,
            saveResultEntity.parentId,
        ])
        conn.commit()  #提交事务，只有提交了才生效，成功提交，失败回滚
        return cursor.lastrowid  #返回插入数据的id
    except Exception as e:
        print(e)
        conn.rollback() #回滚事务
        return 0
    finally:
        LoadMySQLConn().close_mysql_conn(cursor,conn)

