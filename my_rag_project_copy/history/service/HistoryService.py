'''
    本模块是用来保存同一窗口的对话历史记录和查询历史记录等操作
'''
from history.dao.HistoryDao import query_history_menu_by_userid
from history.dao.HistoryDao import query_history_list_by_historyid
from history.dao.HistoryDao import save_chat_results
#根据用户id来显示该用户所有对话窗口历史记录
def query_history_menu(usersId):
    results = query_history_menu_by_userid(usersId)
    #存储历史记录
    data = []
    for item in results:
        data.append({
            "historyId":item["history_id"],
            "question":item["question"],
            "answer":item["answer"],
            "createTime":item["create_time"].strftime("%Y-%m-%d %H:%M:%S"),
        })
    return{
        "code":200,
        "msg":"查询成功",
        "data":data  #返回historyId、question、answer、createTime
    }

#根据根对话历史id查询某个窗口完整的上下文记录和其所有子记录
def query_history_list(historyId:int):
    results = query_history_list_by_historyid(historyId)
    data = []
    for item in results:
        #添加用户问题
        data.append({
            "role":"user",
            "content": item["question"]
        })
        #添加ai根据上述问题的回答
        data.append({
            "role":"assistant",
            "content":item["answer"]
        })
    return{
        "code":200,
        "msg":"查询成功",
        "data":data  #返回该窗口所有之前的历史记录(提出的问题和ai回答)
    }

#保存当前对话到数据库中
def save_chat_result(userId:int,question:str,answer:str,parentId:int):
    history_id = save_chat_results(userId,question,answer,parentId)
    #若数据被存入则history_id一定会生成一个大于0的数
    if history_id>0:
        return{
            "code":200,
            "msg":"当前对话保存数据成功",
            "data":history_id
        }
    else:
        return {
            "code":500,
            "msg":"当前对话保存数据失败",
            "data":None
        }
