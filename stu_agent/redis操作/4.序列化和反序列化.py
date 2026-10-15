import redis
import json
conn = redis.StrictRedis(host="localhost",port=6379,db=0)

user_id = "001"
key = f"xuliehua:{user_id}"

#序列化和反序列化
def serialization():
    user_info = {"name":"张三","age":21}
    #序列化
    data = json.dumps(user_info,ensure_ascii=False)  #ensure_ascii保证JSON字符串的中文保持原样而非\u转义
    conn.set(key,data)
    print(f"获取值：{conn.get(key)}")
    #反序列化
    data = conn.get(key)
    data = json.loads(data)
    print(f"获取值：{data}")

if __name__ == '__main__':
    serialization()