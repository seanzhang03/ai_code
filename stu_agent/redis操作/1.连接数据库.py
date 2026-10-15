import redis
'''
    点赞等
'''
conn = redis.Redis(host="localhost",port=6379,db=0)
print(conn.ping())

# 键名
user_id = "001"
key = f"test:{user_id}"  # 不建议用f"{user_id}"来作键名，可能会被覆盖掉

#字符串
def load_str():
    #存储字符串
    conn.set(key,"helloworld")
    #获取字符串
    rs = conn.get(key)
    print(rs)
    print(type(rs))
    #获取存储的类型
    rs = conn.get(key).decode()  #转换为字符串类型
    print(rs)
    #设置过期时间，ex单位为秒
    conn.set(key,"lisi",ex=30)

def load_init():
    # 初始化为0
    conn.set(key, 0)

#自增，自减
def load_inc():
    conn.incr(key)
    print(f"自增后的值：{conn.get(key).decode()}")

def load_dinc():
    conn.decr(key)
    print(f"自减后的值：{conn.get(key).decode()}")

if __name__ == '__main__':
    #load_str()
    #load_init()
    #load_inc()
    load_dinc()