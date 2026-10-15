import redis

conn = redis.StrictRedis(host="localhost",port=6379,db=0)

user_id = "001"
key = f"test_list:{user_id}"

#从列表添加元素，从左侧添加，右边提取
def load_left_add_right_pop():
    #左侧添加
    conn.lpush(key,"1","2","3")
    #右侧提取
    data = conn.rpop(key)
    print(data.decode())
    #获取提取后
    queue = conn.lrange(key,0,-1)
    print(f"提取后的队列：{queue}")

key1 = f"test_list_right:{user_id}"
#从列表添加元素，从右侧添加，左边提取
def load_right_add_left_pop():
    #右侧添加
    conn.rpush(key1,"a","b","c")
    #左侧提取并删除这个元素
    data = conn.lpop(key1)
    print(data.decode())
    #获取提取后
    queue = conn.lrange(key1, 0, -1)
    print(f"提取后的队列：{queue}")

#删除键名
def del_data(key):
    if conn.exists(key):
        conn.delete(key)
        print("删除成功")
    else:
        print("键不存在")
if __name__ == '__main__':
    # load_left_add_right_pop()
    # load_right_add_left_pop()
    del_data(f"test_list:{user_id}")