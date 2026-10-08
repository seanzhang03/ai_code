from pydantic import Field,BaseModel

class SaveChatResultsEntity(BaseModel):
    userId:str = Field(...,description="用户id")
    question:str = Field(...,description="用户问题")
    answer:str = Field(...,description="ai回答")
    parentId:int = Field(...,description="根对话的历史id")