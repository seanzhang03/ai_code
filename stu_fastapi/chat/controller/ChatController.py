import json
from fastapi import APIRouter
from starlette.responses import StreamingResponse
from chat.service import ChatService

chat_router = APIRouter()

#聊天路由配置
@chat_router.get("/chat")
def chat(question:str,historyId:str):
    def generator():

        for item in ChatService.chat(question,int(historyId)):  #控制流式输出次数
            yield f"data:{json.dumps({"content":str(item)})}\n\n"  #sse数据相应的格式，如果用的是fetch直接写str(item)即可
        yield f"data:{json.dumps({"content":"[DONE]"})}\n\n"  #[DONE]表示结束
    return StreamingResponse(
        content = generator(),
        media_type="text/event-stream" #声明响应的MIME类型为text/event-stream，告诉客户端这是一条SSE流，按事件流方式持续读取，而非当成普通一次性响应
    )