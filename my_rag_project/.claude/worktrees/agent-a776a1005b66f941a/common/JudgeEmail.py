'''
    本模块是用来判断邮箱格式是否合规的
'''
import re
def judge_email(email:str):
    email_format = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    if email_format.match(email):
        return True
    else:
        return False

if __name__ == "__main__":
    print(judge_email("2012761893sean@163.com"))