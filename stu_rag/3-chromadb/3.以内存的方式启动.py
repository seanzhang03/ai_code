#以内存的方式启动chromadb，数据不会持久化保存，用完就丢失，通常不采用
import chromadb
#EphemeralClient：chromadb提供的用于内存启动方式的对象
client = chromadb.EphemeralClient()
print(client)