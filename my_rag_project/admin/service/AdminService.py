'''
    本模块是实现管理员的功能，比如增加用户,密码初始化和删除一个用户
'''
from admin.dao.AdminDao import query_users_by_nickname, password_init_by_nickname, delete_users_by_nickname, \
    create_users_with_email_nickname, query_users_by_email


#增加一个用户，需要给定邮箱和用户名，密码直接初始化为123456
def create_users(email:str,nickname:str):
    email_rs = query_users_by_email(email)
    nickname_rs = query_users_by_nickname(nickname)
    #用户名和邮箱都没有被注册时，才可以进行操作
    if len(email_rs) ==0 and len(nickname_rs)==0:
        try:
            userid = create_users_with_email_nickname(email,nickname)
            print(userid)
            if userid>0:
                print("用户创建成功，初始密码为123456")
                return {
                    "code":200,
                    "msg":"用户创建成功",
                    "data":None
                }
            else:
                print("用户创建失败，请重新创建")
                return {
                    "code":500,
                    "msg":"用户创建失败",
                    "data":None
                }
        except Exception as e:
            print(e)
            print("用户创建失败，请重新创建")
            return {
                "code": 500,
                "msg": "用户创建失败",
                "data": None
            }
    else:
        print("该用户名或邮箱已经存在！创建失败")
        return {
            "code":500,
            "msg":"用户名或邮箱已经存在",
            "data":None
        }


#让一个用户密码初始化
def password_init(nickname:str):
    rs = query_users_by_nickname(nickname)
    if len(rs)>0:
        print("该用户名存在，下面将进行初始化该用户密码")
        password_init_by_nickname(nickname)
        print(f"{nickname}用户已经初始化密码，默认初始化密码为123456！")
        return {
            "code":200,
            "msg":"该用户密码已经初始化",
            "data":None
        }
    else:
        print("用户名不存在，无法进行初始化功能！")
        return {
            "code":500,
            "msg":"用户名不存在，无法进行初始化功能！",
            "data":None
        }

#删除一个用户
def delete_users(nickname:str):
    rs = query_users_by_nickname(nickname)
    if len(rs)>0:
        print("该用户名存在，下面进行删除该用户操作")
        delete_users_by_nickname(nickname)
        print(f"{nickname}用户信息已经删除！")
        return {
            "code":200,
            "msg":"该用户已经被删除",
            "data":None,
        }
    else:
        print("用户名不存在，无法进行初始化功能！")
        return {
            "code": 500,
            "msg": "用户名不存在，无法进行初始化功能！",
            "data": None
        }

if __name__ == "__main__":
    #create_users("2012761893@qq.com","SeanZhang")
    # delete_users("Kate")
    password_init("dddd")

