from pydantic import Field,BaseModel
class SaveResultEntity(BaseModel):
    usersId:int = Field(...,description="用户id")  #
    question:str = Field(...,description="用户问题")
    answer:str=Field(...,description="AI回复")
    parentId:int = Field(...,description="对话保存哪个父级对话")