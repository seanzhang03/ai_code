#验证码生成工具，只考虑数字验证码的生成
import random

class CreateCaptchaUtil:
    def __init__(self):
        self.code = ""
    def create_captcha(self):
        for i in range(4):
            self.code+=str(int(random.random()*10))  #将随机生成的0-9的数来拼接成一个四位的验证码


'''
if __name__ == "__main__":
    a = CreateCaptchaUtil()
    a.create_captcha()
    print(a.code)
'''