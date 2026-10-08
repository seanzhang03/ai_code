from history.dao import HistoryDao

#查询历史记录菜单
def query_history_menu(usersId):
    results = HistoryDao.query_history_menu(usersId)
    #存储历史记录的列表
    data=[]
    for item in results:
        data.append(
            {
                "historyId":item["history_id"],
                "question":item["question"],
                "answer":item["answer"],
                "createTime":item["create_time"].strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    return {
        "code":200,
        "msg":"查询成功",
        "data":data
    }

#根据会话id查询完整历史对话记录
def query_history_list(historyId):
    results = HistoryDao.query_history_list(historyId)
    data=[]
    for item in results:
        #添加用户问题
        data.append({
            "role":"user",
            "content":item["question"]
        })
        #添加ai回答
        data.append({
            "role":"assistant",
            "content":item["answer"]
        })
    return {
        "code":200,
        "msg":"查询成功",
        "data":data

    }


#保存对话结果
def save_chat_result(saveResultEntity):
    results = HistoryDao.save_chat_result(saveResultEntity)
    print(results)
    if results >0:
        return {
            "code":200,
            "msg":"保存成功",
            "data":results
        }
    else:
        return{
            "code":500,
            "msg":"保存失败",
            "data":None
        }

