from common.LoadMySQLConn import LoadMySQLConn
from passlib.context import CryptContext

#创建加密对象---加密算法bcry
crypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")



conn = LoadMySQLConn().conn
sql = "SELECT * FROM users where email=%s"
email = input("请输入邮箱号： \n")
password = input("请输入密码：\n")
cursor = conn.cursor()
cursor.execute(sql,[email])
result = cursor.fetchall()

if len(result):
    mysql_password  = result[0]["password"]  #记得将数据库的密码转换为暗文
    #密码比较
    if crypt_context.verify(password,mysql_password):
        print("登录成功")
    else:
        print("密码错误")
else:
    print("用户不存在")