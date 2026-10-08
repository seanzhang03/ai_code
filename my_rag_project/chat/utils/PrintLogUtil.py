'''
    打印召回、BM25、重排序的结果
'''

def print_log_util(docs,title):
    print(f"{title}")
    for index,doc in enumerate(docs):
        print(f"第{index}个文档：{doc}")