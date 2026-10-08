"""
    这个文件是用来针对于用户模块的业务处理代码实现
"""
import os
from zuoye.dao import UsersDao
# 导入邮件发送需要的类
from email.mime.text import MIMEText
import smtplib
# 验证码生成工具
from zuoye.utils.CreateCaptchaUtil import CreateCaptchaUtil
# redis
from common.LoadRedisConn import LoadRedisConn


# 发送验证码
def send_captcha(email):
    # 1、通过邮箱先获取到对应的数据
    results = UsersDao.query_users_by_email(email)
    # 2、根据查询的结果判定是否满足登录的条件 --- 未注册不允许登录
    if len(results) == 0:
        return {
            "code": 500,
            "msg": "邮箱未注册",
            "data": None
        }
    # 3、创建邮件对象 --- 这个对象是用来存储发送邮件信息的【信封】
    send_email = os.getenv("SEND_EMAIL")  # 发件人信息
    send_email_code = os.getenv("SEND_EMAIL_CODE")  # 授权码信息
    subject = "欢迎使用法律问答助手"  # 邮件的主题
    code = CreateCaptchaUtil().code
    content = f"你本次登录的验证码是：{code},过期时间为60s"
    message = MIMEText(content, "plain", "utf-8")  # 通过content创建邮件对象
    message["From"] = send_email  # 把发件人信息写入
    message["To"] = email  # 把收件人信息写入
    message["Subject"] = subject  # 把邮件主题写入
    # 4、连接QQ邮箱服务器
    smtp_server = os.getenv("SMTP_SERVER")  # 邮箱服务器地址
    smtp_port = int(os.getenv("SMTP_PORT"))  # 邮件服务器端口
    smtp = smtplib.SMTP(smtp_server, smtp_port)  # 创建邮件发送实例
    smtp.starttls()  # 启动TLS加密 --- TLS对应的端口是587
    smtp.login(send_email, send_email_code)  # 校验发件人信息
    smtp.sendmail(send_email, email, message.as_string())  # 发送邮件
    smtp.quit()  # 关闭邮件连接
    # 5、把验证码存入到redis中 --- 通过key value格式存储数据，key要唯一，否则值被覆盖
    try:
        redis_conn = LoadRedisConn.load_redis_conn()
        redis_conn.setex(email, 60, code)  # 存储数据 --- key为email，value为code，60s后过期
        LoadRedisConn.close_redis_conn(redis_conn)
        return {
            "code": 200,
            "msg": "验证码已发送",
            "data": None
        }
    except Exception as e:
        print(f"验证码发送失败：{e}")
        return {
            "code": 500,
            "msg": "验证码发送失败",
            "data": None
        }


# 验证码登录
def login(email, code):
    # 1、从redis中获取验证码
    try:
        redis_conn = LoadRedisConn.load_redis_conn()
        redis_code = redis_conn.get(email)  # 获取验证码
        LoadRedisConn.close_redis_conn(redis_conn)

        # 2、判断验证码是否正确
        if redis_code is None:
            return {
                "code": 500,
                "msg": "验证码已过期，请重新获取",
                "data": None
            }

        if redis_code != code:
            return {
                "code": 500,
                "msg": "验证码错误",
                "data": None
            }

        # 3、获取用户信息
        results = UsersDao.query_users_by_email(email)
        if len(results) == 0:
            return {
                "code": 500,
                "msg": "用户不存在",
                "data": None
            }

        # 4、删除redis中的验证码（一次性使用）
        redis_conn = LoadRedisConn.load_redis_conn()
        redis_conn.delete(email)
        LoadRedisConn.close_redis_conn(redis_conn)

        # 5、返回用户信息（包含昵称）
        user = results[0]
        return {
            "code": 200,
            "msg": "登录成功",
            "data": {
                "id": user.get("id"),
                "email": user.get("email"),
                "nickname": user.get("nickname"),
                "avatar": user.get("avatar", "")
            }
        }
    except Exception as e:
        print(f"登录失败：{e}")
        return {
            "code": 500,
            "msg": "登录失败，请重试",
            "data": None
        }