'''
    该模块是将未注册的用户进行注册时，操作数据库的具体代码
'''
from common.LoadMySQLConn import LoadMySQLConn
from common.JWTUtil import hash_password
#保存用户注册信息
def save_registration_result(email:str,password:str,nickname:str):
    conn = LoadMySQLConn().conn
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO users VALUES(NULL,%s,%s,%s,now(),%s)"  #user_id赋值NULL进行自动自增，create_time用now()来获取当前时间
        cursor.execute(sql,[
            email,
            hash_password(password),
            nickname,
            "user"
            ])
        conn.commit() #提交事务
        return cursor.lastrowid  #返回插入数据id
    except Exception as e:
        print(e)
        conn.rollback()  #回滚事务
        return 0

if __name__ == "__main__":
    from pydantic import Field, BaseModel
    class RegistrationUsers(BaseModel):
        # 邮箱号
        email: str = Field(..., description="邮箱号")
        # 用户名
        nickname: str = Field(..., description="用户名")
        # 密码
        password: str = Field(..., description="密码")
    rs = RegistrationUsers(email="1607259232@qq.com",nickname="seanzhang",password="123456")
    save_registration_result(rs)