'''
    该模块是实现用户注册功能的部分
'''
from registration.dao.RegistrationDao import save_registration_result
from login.dao.LoginDao import query_users_by_email,query_users_by_nickname
from pydantic import Field,BaseModel
from common.JudgeEmail import judge_email
from common.JWTUtil import hash_password,verify_password
#用户注册
def registration(email:str,password:str,nickname:str):  #传3个字符串进来
    #查询该邮件是否注册
    email_results = query_users_by_email(email)
    nickname_results = query_users_by_nickname(nickname)
    print()
    #邮箱未注册则进行注册功能
    if len(email_results) == 0 and len(nickname_results)==0:  #邮箱号和昵称都不能和数据库中有的一致
        if judge_email(email) == False:
            print("邮箱格式不正确！请重新输入")
            return {
                "code":500,
                "msg":"邮箱格式不正确",
                "data":None
            }
        elif judge_email(email) == True:
            try:
                #数据库入库操作
                save_registration_result(email,hash_password(password),nickname)
                email_rs = query_users_by_email(email)
                nickname_rs = query_users_by_nickname(nickname)
                if len(email_rs) != 0 and len(nickname_rs)!=0:  #email和nickname都入库了才显示注册成功
                    print("注册成功")
                    return{
                        "code":200,
                        "msg":"注册成功",
                        "data":None
                    }
            except Exception as e:
                print(f"注册失败:{e}")
                return {
                    "code":500,
                    "msg":"注册失败，请重新注册",
                    "data":None,
                }
    #邮箱已注册则拒绝注册
    else :
        print("该邮箱或用户名已经注册！请回到登录页面直接登录。")
        return {
            "code":500,
            "msg":"该邮箱或用户名已经注册",
            "data":None
        }

if __name__ == "__main__":

    registration(email="12345632112@qq.com",nickname="ddddd",password="123456")
