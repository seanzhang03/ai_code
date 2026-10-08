#导入schemas模块中的类
from schemas.users import *   #*表示导入模块中所有内容（类、变量、方法）
from models.user import *

def create_new_user(user: UserCreate):  #在schemas中创建python文件，users.py黄健数据响应模型UserCreate类（接收前端到后端python到数据）
    #操作数据库
    global next_id  #获取next_id的值
    new_user = {"id":next_id,**user.model_dump()}
    print(f"新建的user用户:",new_user)
    user_db[next_id] = new_user
    next_id+=1
    print(f"添加到字典中的user值：",user_db)
    return new_user


#定义一个方法，根据ID查找用户
def get_user(id:int)->dict:
    user = user_db.get(id)
    return user