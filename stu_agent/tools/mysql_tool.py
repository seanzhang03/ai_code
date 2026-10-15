from dotenv import load_dotenv
import os
from pydantic import BaseModel,Field
from langchain.tools import tool
import pymysql

load_dotenv()

class MysqlParams(BaseModel):
    sql:str =Field(...,description="sql语句")

@tool(args_schema=MysqlParams)
def mysql_tool(sql:str)->str: #可以在功能描述里添加增删改功能
    """
    执行sql查
    数据库模式：
        user_info 用户信息表 
        字段：
        user_id:用户id
        user_name:用户名
        email:邮箱
        department:部门
    """
    #数据连接
    conn =None
    #游标
    cursor = None
    try:
        #读取配置
        db_host = os.getenv("MYSQL_HOST")
        db_port = os.getenv("MYSQL_PORT")
        db_user = os.getenv("MYSQL_USER")
        db_password = os.getenv("MYSQL_PASSWORD")
        db_name = os.getenv("MYSQL_NAME")
        if not db_host or not db_port or not db_user or not db_password or not db_name:
            return "请检查数据库配置"
        if sql.startswith("DELETE"): #即使提示词允许删除，这里写死了禁止执行
            return "禁止执行"
        conn = pymysql.connect(
            host=db_host,
            port=int(db_port),
            user=db_user,
            password=db_password,
            db=db_name,
            charset="utf8"
        )
        print(conn)
        #创建游标对象
        cursor = conn.cursor()
        #执行sql
        cursor.execute(sql)
        #获取结果
        rs = cursor.fetchall()
        # #事务提交
        # conn.commit()
        return str(rs)
    except Exception as e:
        print(f"出现异常{e}")
        return "数据库出现异常了"
    finally:
        #资源释放
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    rs = mysql_tool.invoke(
        {"sql":"select * from user_info"}
    )
    print(rs)