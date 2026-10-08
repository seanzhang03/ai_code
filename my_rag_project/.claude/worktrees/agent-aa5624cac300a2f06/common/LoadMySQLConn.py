import os

import pymysql
from dotenv import load_dotenv

load_dotenv()


class LoadMySQLConn:
    def __init__(self):
        self.conn = self.load_mysql_conn()

    @staticmethod
    def load_mysql_conn():
        return pymysql.connect(
            host = os.getenv("MYSQL_HOST"),  #MySQLip地址
            user = os.getenv("MYSQL_USER"),  #mysql用户名
            password=os.getenv("MYSQL_PASSWORD"),  #mysql连接密码
            database=os.getenv("MYSQL_DATABASE"),  #数据库名称
            charset="utf8mb4",  #字符编码
            cursorclass= pymysql.cursors.DictCursor  #查询结果以字典格式返回
        )

    @staticmethod
    def close_mysql_conn(cursor,conn):
        cursor.close()
        conn.close()

