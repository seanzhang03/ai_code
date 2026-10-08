'''
    验证码生成工具，通过本工具生成一个随机的六位验证码
'''
import random

class CreateCaptchaUtil:
    def __init__(self):
        self.captcha = self.create_captcha()

    @staticmethod
    def create_captcha():
        captcha = ""
        for i in range(6):
            captcha+=str(int(random.random()*10))  #随机生成的0~9的数拼接成一个六位验证码
        return captcha

if __name__ =="__main__":
    a = CreateCaptchaUtil()
    print(a.captcha)