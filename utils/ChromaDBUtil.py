import chromadb
#定义获取chromadb连接对象的函数
def get_chromadb_conn(path):  #创建Chroma的持久实例并保存到磁盘，返回的是一个客户端API
    return chromadb.PersistentClient(path=path)
