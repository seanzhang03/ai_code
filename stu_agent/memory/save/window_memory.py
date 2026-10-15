import redis
from dotenv import load_dotenv
import os

load_dotenv()
"""
    窗口记忆，记录最近的4轮窗口记忆
"""
class WindowMemory:
    def __init__(self,session_id:int):
        self.client =redis.StrictRedis(host="localhost",port=6379,db=0)
        #设置key
        key = f"chat_window:{session_id}"
        #获取轮次
        self.window_size=os.getenv("WINDOWS_SIZE")

    #添加记忆
    def add_memory(self,role:str,content):