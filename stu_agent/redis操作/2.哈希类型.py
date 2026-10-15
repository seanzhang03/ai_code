import redis
conn = redis.Redis(host="localhost",port=6379,db=0)

user_id = "001"
key = f"test_hash:{user_id}"
#hash创建
def load_hash():
    conn.hset(key,"user_id",1)
    conn.hset(key,"user_name","李四")
    conn.hset(key,"email","111@qq.com")
    conn.hset(key,"department","技术部")
    print("哈希创建成功")

#hash获取
def get_hash():
    print(conn.hget(key,"user_name").decode())

if __name__ == '__main__':
    load_hash()
    get_hash()