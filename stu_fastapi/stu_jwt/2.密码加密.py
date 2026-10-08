#这是一个密码加密的示例
#1.加密
#2.验证
from passlib.context import CryptContext

#创建加密对象--加密算法bcrypt
crypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#密码加密函数
def hash_password(password)->str:
    return crypt_context.hash(password)

#密码验证函数
def verify_password(plain_password:str,hashed_password:str)->bool:
    return crypt_context.verify(plain_password,hashed_password)

if __name__=="__main__":
    hashed_password=hash_password("654321") #加密
    print(f"加密后的密码：{hashed_password}")
    result = verify_password("111",hashed_password)#验证
    print(f"验证结果:{result}")

