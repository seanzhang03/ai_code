'''
    操作历史记录的路由
'''
from fastapi import APIRouter
from history.service import HistoryService
from history.entity.HistoryEntity import SaveChatResultsEntity
history_router = APIRouter()

#根据用户id来显示该用户所有对话窗口历史记录
@history_router.get("/queryHistoryMenu/{usersId}")
def query_history_menu(usersId:int):
    return HistoryService.query_history_menu(usersId)

#根据历史id查询某个窗口完整的上下文记录和其所有子记录
@history_router.get("/queryHistoryList/{historyId}")
def query_history_list(historyId:str):
    return HistoryService.query_history_list(historyId)

#保存对话记录
@history_router.post("/saveChatResult")
def save_chat_result(save_chat_results_entity:SaveChatResultsEntity):
    return HistoryService.save_chat_result(
        int(save_chat_results_entity.userId),
        save_chat_results_entity.question,
        save_chat_results_entity.answer,
        int(save_chat_results_entity.parentId)
        )