import redis
import os
from dotenv import load_dotenv

load_dotenv()

class LoadRedisConn:
    def __init__(self):
        self.conn = self.load_redis_conn()

    @staticmethod
    def load_redis_conn():
        return redis.Redis(
            host=os.getenv("REDIS_HOST"),  #数据库服务器的ip
            port=os.getenv("REDIS_PORT"),  #端口号
            password=os.getenv("REDIS_PASSWORD"),  #连接密码---root账号对应密码
            db=os.getenv("REDIS_DATABASE"),  #操作数据库名称
            decode_responses=True,  #解码响应结果为字符串，否则字节
        )

    #关闭redis连接
    @staticmethod
    def close_redis_conn(conn):
        conn.close()
