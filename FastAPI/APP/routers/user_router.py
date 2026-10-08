from fastapi import APIRouter,status,HTTPException
from service.user_service import *
from schemas.users import *

#创建路由
router = APIRouter()


#定义一个创建用户的方法
@router.post("/users",status_code = status.HTTP_201_CREATED)
async def create_user(user:UserCreate):
    return create_new_user(user)

#定义一个路由，用来执行查询数据库中用户的数据
@router.get("/user/{user_id}")
async def get_user_id(user_id:int)->dict:
    user = get_user(user_id)
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"用户{user_id}不存在!")
    return user

#HTTP状态码
#成功响应：
# 状态码     FastAPI中常量名              解析                                      使用场景
# 200        HTTP_200_OK         请求成功时，响应体包含的内容             get读取资源、put/patch更新资源，post添加数据成功
# 201        HTTP_201_CREATED    新建资源成功时相应的内容                 Post请求创建数据成功
# 202        HTTP_202_ACCEPTED   请求已被接收，但是未完成处理             邮件发送、文件发送
# 204        HTTP_204_NO_CONTENT 操作成功，无相应内容                     DELETE删除成功、PUT更新成功无需返回响应体
#重定向
# 301        HTTP_301_MOVED_     资源路径已被更新，即将废弃该资源路径，迁移到新URL地址  API废弃或域名即将更换
#            PERMANENTLY
# 302        HTTP_302_FOUND      临时重定向
#客户端错误
# 400        HTTP_400_BAD_       前端请求参数不合法     
#            REQUEST                  
# 401        HTTP_401_           权限未认证                               TOKEN认证
#            UNAUTHORIZED           
# 403        HTTP_403_FORBIDDEN  权限不足                                 会员、超级会员
# 404        HTTP_404_NOT_FOUND  查找资源不存在
# 405        HTTP_405_NOT_ALLOWED请求方法错误、不允许                      API使用app.get，前端客户端axios(post="")
# 408        HTTP_408_TIMEOUT    请求超时                                 网络加载失败或者网络不稳定
# 409        HTTP_409_CONFILICT  重复创建唯一标识                          
# 410        HTTP_410            请求资源不存在                           数据库删除数据，但是前端界面还未消失
# 413        HTTP_413            请求资源过大，超出服务器带宽
# 415        HTTP_415            提交数据不合法，提交JSON数据Content-type:application/json
# 429        HTTP_429            请求频率过快
#服务器错误
# 500        HTTP_500            服务器错误
# 503        HTTP_503            服务不可用                               后端宕机
# 504        HTTP_504            请求资源过慢、网络过慢、数据库较大加载过慢
#                                IO文件加载过慢导致请求时间超时