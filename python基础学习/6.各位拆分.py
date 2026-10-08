#对输入的数进行各位拆分
num =int(input("请输入一个整数")) #int将input括起来，可以将input视为一个函数
gewei = num % 10
shiwei = num // 10 % 10  #注意python里面一定要用整除
baiwei = num // 100 % 10
print("个位为",gewei,"十位为",shiwei,"百位为",baiwei)