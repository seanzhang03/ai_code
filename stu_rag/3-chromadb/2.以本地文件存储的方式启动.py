#chromaDB的数据存储在指定文件夹中，直接去访问使用无需7中，先通过chromadb启动服务器，再连接服务器，本地开发最常用的方案
import chromadb
#PersistentClient：本地文件存储的方式获取操作chromadb的对象
#参数path：指定数据存储的文件夹路径
client = chromadb.PersistentClient(path="../../chroma_data/test2")
print(client)