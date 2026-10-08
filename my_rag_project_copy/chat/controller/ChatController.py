'''
    对话的路由
'''

import json

from fastapi import APIRouter
from chat.service import ChatService
from starlette.responses import StreamingResponse

chat_router = APIRouter()

#对话路由配置
@chat_router.get("/chat")
def chat(question:str,historyId:str):
    def chat_generator():
        for item in ChatService.chat(question,int(historyId)):  #控制流式输出
            #json.dumps将python对象序列化为JSON格式字符串
            yield f"data:{json.dumps({"content":str(item)})}\n\n"  #\n\n是sse数据对应的格式，每条数据后面都要加，若是fetch则直接写str(item)
        yield f"data:{json.dumps({"content":"[DONE]"})}\n\n"  #[DONE]表示结束
    return StreamingResponse( #StreamingResponse是fastapi中流式传输响应的类，允许数据分块发送给客户端
        content = chat_generator(),
        media_type="text/event-stream" #声明响应的MIME类型为text/event-stream，告诉客户端这是一条SSE流，按事件流方式持续读取，而不是普通的一次性响应
    )