import redis
import os
from dotenv import load_dotenv

load_dotenv()

class LoadRedisConn:
    def __init__(self):
        self.conn = self.load_redis_conn()


    # 加载redis连接
    @staticmethod
    def load_redis_conn():
        return redis.Redis(          #connect返回一个connection对象
            host=os.getenv("REDIS_HOST"),  # 数据库服务器的ip
            port=os.getenv("REDIS_PORT"),  # 连接账号
            password=os.getenv("REDIS_PASSWORD"),  # 连接密码 --- root账户对应的密码
            db=os.getenv("REDIS_DATABASE"),  # 操作的数据库名称
            decode_responses=True, #解码响应结果为字符串，否则为字节
        )

    #关闭redis连接
    @staticmethod
    def close_redis_conn(conn):
        conn.close()