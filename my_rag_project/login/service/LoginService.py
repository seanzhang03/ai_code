'''
    本模块实现用户的登录和通过验证码,若用户没有注册，则跳转到注册界面
'''
import os

from login.dao import LoginDao
from dotenv import load_dotenv
from login.utils.CreateCaptchaUtil import CreateCaptchaUtil
from email.mime.text import MIMEText
from common.LoadRedisConn import LoadRedisConn
import smtplib
from common.JWTUtil import verify_password
from common.JWTUtil import create_token

load_dotenv()

def send_captcha(email):
    #1.通过邮箱获取到对应数据
    results = LoginDao.query_users_by_email(email)  #返回数据库内的数据
    #2.根据查询结果判定是否有登录条件，若未注册，返回信息并跳转到对应注册页面
    if len(results) == 0:
        print("该邮箱未注册")
        return {
            "code":500,
            "msg":"邮箱未注册",
            "data":None
        }
    #3.创建邮件对象的相关信息
    #发件人信息
    send_email=os.getenv("SEND_EMAIL")
    #授权码信息
    auth_code = os.getenv("AUTH_CODE")
    #邮件主题
    subject = "您正在通过邮箱进行影视问答系统的登录"
    #实例化对象并调用
    create_captcha_util = CreateCaptchaUtil()
    captcha = create_captcha_util.captcha
    print(captcha)
    content =f"你本次登录的验证码为{captcha}，过期时间为5分钟"
    messages = MIMEText(content,"plain","utf-8") #MIMEText用于创建纯文本或HTML格式的邮件正文，plain表示纯文本
    messages["From"] = send_email  #写入发件人信息
    messages["To"] = email #写入收件人信息
    messages["Subject"] = subject  #写入邮件主题
    #4.连接qq邮箱服务器
    smtp_server = os.getenv("SMTP_SERVER")  #邮箱服务器地址
    smtp_port = os.getenv("SMTP_PORT")  #邮箱服务器端口
    smtp = smtplib.SMTP(smtp_server,smtp_port)  #创建邮件发送的对象实例，连接到邮件服务器
    smtp.starttls()  #启动TLS加密---TLS对应端口为587， TLS是传输层的一个加密协议
    smtp.login(send_email,auth_code)  #校验发件人信息
    smtp.sendmail(send_email,email,messages.as_string())  #将MIMEText对象转成符合邮件协议的字符串，里面包含from，to和subject的base64编码等
    smtp.quit()  #关闭邮件连接
    #5.将验证码放到redis中--通过键值对格式存储数据，键要唯一，否则值被覆盖
    try:
        redis_conn = LoadRedisConn.load_redis_conn()
        redis_conn.setex(email,300,captcha)  #存储数据---key是email，value是captcha，五分钟过期
        LoadRedisConn.close_redis_conn(redis_conn)
        print("验证码已经发送！")
        return{
            "code":200,
            "msg":"验证码已发送",
            "data":{
                "nickname":results[0]["nickname"],    #results是查询到的指定邮箱的mysql数据库里的用户信息，其本质是一个列表，列表的第一个元素是一个包含信息的键值对
                "usersId":results[0]["users_id"]
            }
        }
    except Exception as e:
        print(f"验证码发送失败！具体原因：{e}")
        return{
            "code":500,
            "msg":"验证码发送失败",
            "data":None
        }

#通过邮箱和验证码登录
def login_by_email_captcha(email,captcha):
    results = LoginDao.query_users_by_email(email)
    #通过email在redis中取值，再判定，没有值表示验证码过期
    redis_conn = LoadRedisConn().conn
    #通过key:email来取验证码value:captcha
    redis_captcha = redis_conn.get(email)
    if not redis_captcha:   #若验证码不存在
        return{
            "code":500,
            "msg":"验证码已过期",
            "data":None
        }
    #比对redis中的captcha和用户输入的captcha
    if redis_captcha == captcha:
        token = create_token({
            "users_id": results[0]["users_id"],
            "nickname": results[0]["nickname"],
            "role": results[0]["role"]
        })
        return{
            "code":200,
            "msg":"登录成功",
            "data":{
                    "usersId": results[0]["users_id"],
                    "nickname": results[0]["nickname"],
                    "role": results[0]["role"]
                },
            "token":token
        }
    return {
        "code":500,
        "msg":"验证码错误",
        "data":None
    }

#通过邮箱和保存的密码登录
def login_by_email_password(email:str,password:str):
    results = LoginDao.query_users_by_email(email)
    if len(results) ==0:
        print("您输入的邮箱未注册！")
        return {
            "code":500,
            "msg":"邮箱未注册",
            "data":None
        }
    else:
        if verify_password(password,results[0]["password"]):
            results = LoginDao.query_users_by_email(email)
            print(results)
            token = create_token({
                "users_id": results[0]["users_id"],
                "nickname": results[0]["nickname"],
                "role": results[0]["role"]
            })
            print("登录成功!")
            return {
                "code":200,
                "msg":"登录成功",
                "data":{
                    "usersId": results[0]["users_id"],
                    "nickname": results[0]["nickname"],
                    "role": results[0]["role"]
                },
                "token":token,
            }
        else:
            print("密码错误！请重新登陆。")
            return {
                "code":500,
                "msg":"密码错误",
                "data":None
            }


#通过用户名和保存的密码登录
def login_by_nickname_password(nickname:str,password:str):
    results = LoginDao.query_users_by_nickname(nickname)
    if len(results) == 0:
        print("您输入的用户名未注册！")
        return {
            "code": 500,
            "msg": "用户名未注册",
            "data": None
        }
    else:
        if verify_password(password,results[0]["password"]):
            results = LoginDao.query_users_by_nickname(nickname)
            token = create_token({
                "users_id": results[0]["users_id"],
                "nickname": results[0]["nickname"],
                "role": results[0]["role"]
            })
            print(token)
            print("登录成功!")
            return {
                "code": 200,
                "msg": "登录成功",
                "data": {
                    "nickname": results[0]["nickname"],
                    "usersId": results[0]["users_id"],
                    "role": results[0]["role"]
                },
                "token":token
            }
        else:
            print("密码错误！请重新登陆。")
            return {
                "code": 500,
                "msg": "密码错误",
                "data": None
            }

if __name__ == '__main__':
    print(login_by_email_password("123456@qq.com","123456"))