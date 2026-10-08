from history.service import HistoryService
from fastapi import APIRouter
from history.entity.SaveResultEntity import SaveResultEntity

history_router = APIRouter()

#查询历史记录菜单
@history_router.get("/queryHistoryMenu/{usersId}")
def query_history_menu(usersId:str):
    return HistoryService.query_history_menu(int(usersId))

#根据会话id查询完整历史对话记录
@history_router.get("/queryHistoryList/{historyId}")
def query_history_list(historyId:str):
    return HistoryService.query_history_list(int(historyId))

#保存对话结果
@history_router.post("/saveChatResult")
def save_chat_result(saveResultEntity:SaveResultEntity):
    return HistoryService.save_chat_result(saveResultEntity)