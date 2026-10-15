from dotenv import load_dotenv
import os
from pydantic import BaseModel,Field
from langchain.tools import tool
from email.mime.text import MIMEText
import smtplib

class EmailEntity(BaseModel):
    to_email:str = Field(...,description="收件人邮箱")
    subject:str =  Field(...,description="邮件主题")
    content:str = Field(...,description="邮件内容")

load_dotenv()

@tool("send_email_tool",args_schema=EmailEntity)
def send_email_tool(to_email:str,subject:str,content:str)->str: #必须要有功能描述，否则无法使用
    """
    功能描述：发送邮件，发送信息，发送通知
    """
    try:
        #邮件配置
        server = os.getenv("SMTP_SERVER")  #smtp的ip
        port = os.getenv("SMTP_PORT")  #smtp端口
        auth_code = os.getenv("AUTH_CODE") #授权码
        send_email = os.getenv("SEND_EMAIL") #发件人邮箱
        if not server or not port or not auth_code or not send_email:
            return "邮件配置有误"
        #1.创建邮件对象，并引入正文
        msg = MIMEText(content)
        #2.收件人
        msg["To"] = to_email
        #3.标题
        msg["Subject"] = subject
        #4.发件人
        msg["From"] = send_email
        #5.登录邮件服务器
        with smtplib.SMTP_SSL(server,int(port)) as smtp:  #SMTP和SMTP_SSL的加密方式不同
            #登录
            smtp.login(send_email,auth_code)
            #发送邮件
            smtp.sendmail(send_email,to_email,msg.as_string())
        return "邮件发送成功"
    except Exception as e:
        print(f"出现异常{e}")
        return "发送邮件出现异常了"
if __name__ == '__main__':
    rs=send_email_tool.invoke({
        "to_email":"2012761893@qq.com",
        "subject":"测试邮件",
        "content":"测试邮件内容"
    })
    print(rs)