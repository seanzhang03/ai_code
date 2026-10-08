#这个文件是用来针对于用户模块的业务处理代码的实现

import os

#导入加载环境变量的方法
from dotenv import load_dotenv
load_dotenv()

from users.dao import UsersDao  #导入类而不导入方法的原因，因为要区分自调用和引入调用，query_users_by_email在库里有
#导入邮件发送需要的类
from email.mime.text import MIMEText
import smtplib

#导入生成验证码模块的生成验证码方法
from users.utils.CreateCaptchaUtil import CreateCaptchaUtil

#导入redis
from common.LoadRedisConn import LoadRedisConn

#导入向量数据库
from common.LoadChromaConn import LoadChromaConn

#导入提示词
from langchain_core.prompts import PromptTemplate

#构造链的工具
from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda

#导入重排序模型
from common.LoadRerankerModel import LoadRerankerModel

#给qq邮箱发送邮件步骤：
#1.配置授权码，授权码是发件方的，收件方不需要
#2.通过qq邮箱服务器发送邮件步骤
#(1).构建邮件对象
#(2).连接邮件服务器
#(3).发送邮件

#发送验证码
def send_captcha(email):  #email为收件人的邮箱
    #1.通过邮箱先获取到对应数据
    results = UsersDao.query_users_by_email(email)  #返回的是数据库里面的数据[{'users_id': 1, 'email': '2012761893@qq.com', 'password': '123456', 'nickname': 'seanzhang', 'create_time': datetime.datetime(2026, 9, 7, 14, 40, 28)}]
    print(results)
    #2.根据查询的结果判定是否有满足登录的条件，没有注册不让登录
    if len(results) == 0:
        print("该邮箱未注册")
        return{
            "code":500,
            "msg":"邮箱未注册",
            "data":None
        }
    #3.创建邮件对象 --- 这个对象是来存储发送邮件信息的
    #发件人信息
    send_email=os.getenv("SEND_EMAIL")  #env文件中的是发件人邮箱，而数据库中是收件人邮箱
    #授权码信息
    auth_code=os.getenv("AUTH_CODE")
    #邮件的主题
    subject = "欢迎使用法律问答助手"
    #实例化一个对象并调用生成验证码的方法
    create_captcha_util = CreateCaptchaUtil()
    create_captcha_util.create_captcha()
    code = create_captcha_util.code
    content = f"你本次登录的验证码为{code},过期时间60s"
    messages = MIMEText(content,"plain","utf-8") #通过content创建邮件对象，该对象用来存储发送邮件
    messages["From"] = send_email  #把发件人信息写入
    messages["To"] = email  #把收件人信息写入
    messages["Subject"] = subject  #把邮件主题写入
    #4.连接QQ邮箱服务器
    smtp_server = os.getenv("SMTP_SERVER")  #邮箱服务器地址
    smtp_port = int(os.getenv("SMTP_PORT"))  #邮箱服务器端口
    smtp = smtplib.SMTP(smtp_server,smtp_port)  #创建邮件发送的对象实例
    smtp.starttls()  #启动TLS加密---TLS对应端口威威587 TLS：传输层的一个协议
    smtp.login(send_email,auth_code)  #校验发件人信息
    smtp.sendmail(send_email,email,messages.as_string())  #发送邮件 as_string()将整个格式化后的消息以字符串的形式返回
    print(messages.as_string())
    smtp.quit()  #关闭邮件连接
    #5.把验证码存到redis中--通过key value格式存储数据，key要唯一，否则值被覆盖
    try:
        redis_conn = LoadRedisConn.load_redis_conn()
        redis_conn.setex(email,60,code)  #存储数据---key为email，value为code(验证码)，60s后过期
        LoadRedisConn.close_redis_conn(redis_conn)
        print("验证码已发送")
        return {
            "code":200,
            "msg":"验证码已发送",
            "data":{
                "nickname":results[0]["nickname"],
                "usersId":results[0]["users_id"]
            }  #列表的第0个元素就是一个字典，包含mysql数据库里面的键值对，
        }
    except Exception as e:
        print(f"验证码发送失败：{e}")
        return{
            "code":500,
            "msg":"验证码发送失败",
            "data":None
        }

#登录
def login(email,captcha):
    #先通过email在redis中取值，然后判定，没有值就表示验证码过期
    redis_conn = LoadRedisConn.load_redis_conn()
    redis_captcha = redis_conn.get(email)
    if not redis_captcha:  #验证码不存在
        return{
            "code":500,
            "msg":"验证码已过期",
            "data":None
        }
    #把redis中取出来的密码和用户输入的密码进行比较
    if redis_captcha == captcha:
        return{
            "code":200,
            "msg":"登录成功",
            "data":None

        }
    return {
        "code":500,
        "msg":"验证码错误",
        "data":None
    }

# #聊天
# def chat(question):
#     #向量数据库连接对象
#     vector = LoadChromaConn().conn
#     #重排序模型对象
#     reranker_model =  LoadRerankerModel().load_reranker_model()
#     #提示词
#     qa_prompt="""
#     你是一个专业的知识库问答助手。你的所有回答必须且只能基于下方【参考上下文】中提供的信息。
#     【核心原则】
#     1. 忠实原文：答案必须完全来源于【参考上下文】，严禁使用外部知识、常识或训练数据补充回答。
#     2. 明确拒答：若【参考上下文】中不包含回答问题所需的信息，请直接回复"根据当前参考资料，未找到相关信息"，严禁编造、推测或模糊作答。
#     3. 精准引用：回答中涉及的关键事实、数据或定义，需在句末标注来源片段编号，格式为 [片段n]。
#     4. 简洁聚焦：直接回答问题本身，不输出开场白、寒暄、总结或与问题无关的背景介绍。
#     5. 保持原意：不得对上下文内容进行过度解读、主观评价或情感渲染，保持客观中立。
#     【回答规范】
#     - 若答案跨越多个片段，需综合整理后连贯表述，并标注所有相关片段编号。
#     - 若上下文存在矛盾信息，优先采用更具体、更新的内容，并注明差异。
#     - 若问题超出上下文范围但可部分回答，仅回答可验证的部分，并明确说明剩余部分无依据。
#     - 代码、命令、专有名词等保持原文大小写与格式不变。
#     【参考上下文】
#     {context}
#     【用户问题】
#     {question}
#     """
#     prompt = PromptTemplate(template=qa_prompt,input_variables=["context","question"])
#     #构造qa链
#     qa_chain = (
#         RunnableParallel({  #并行计算，这里将两个值给到context和question
#             "context":vector.as_retriever(),  #基于检索器检索文档作为context的值
#             "question":RunnablePassthrough()  #传递问题作为question的值 --- 透明传递
#
#         })
#     )


if __name__ == "__main__":
    send_captcha("2012761893@qq.com")
