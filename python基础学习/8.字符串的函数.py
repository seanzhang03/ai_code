#字符串的查询函数/转换函数/判断函数/分割函数/其他函数

#查询函数
#find()检测字符串是否包含指定字符，是则返回开始的索引，否则返回-1
#返回索引返回找到的第一个字符的索引
str1="hello world"
print(str1.find("l"))
print(str1.find("ab"))
#index函数一样，只有没找到的时候会将-1改为报错
print(str1.index("l"))
#print(str1.index("ab"))
#rfind和rindex函数从右到左检测
print(str1.rfind("l"))
print(str1.find("or"))
print(str1.rfind("or"))

#字符串转换函数（操作对象是字母）
#upper()将字符串中的小写字母转换成大写字母
#lower()将字符串中的大写字母转换成小写字母
#title()将字符串中的每个单词的第一个字母转换成大写字母，其他字母转换成小写字母
print(str1.upper())
print(str1.lower())
print(str1.title())
#字符串判断函数
#startswidth()判断字符串是否以指定字符串开头，是则返回True，否则返回False
print(str1.startswith('he'))
print(str1.startswith('ll'))
#endswidth()判断字符串是否以指定字符串结尾，是则返回True，否则返回False
print(str1.endswith('ld'))
print(str1.endswith('or'))
#isspace()判断字符串是否只包含空格，是则返回True，否则返回False
print(str1.isspace())
#isalnum()判断字符串是否只包含数字和字母，是则返回True，否则返回False
print(str1.isalnum())
#isdigit()判断字符串是否只包含数字，是则返回True，否则返回False
print(str1.isdigit())
#isalpha()判断字符串是否只包含字母，是则返回True，否则返回False
print(str1.isalpha())

#分割函数
#partition()将字符串分割成3个部分，分别是分割符之前的部分、分割符、分割符之后的部分
#生成的每个部分都是一个元组
#如果参数填写的字符串不存在，则会生成两个空字符串和原字符串
print(str1.partition("llo"))
#rpartition()与partition()功能一样，只是从右向左进行分割
print(str1.rpartition("llo"))
#split()将字符串分割成多个部分,partition()函数只检测到一个，而该函数则检测到所有的
print(str1.split("l"))  #分割后是list，同时所给参数不会分配到对应的list中去
print(str1.split("l",2)) #可以自定义切割次数，若未定义则切割所有部分
#split函数若不传参数则会分割空格或者制表符等
#splitlines()将字符串按行进行分割，返回一个list
print(str1.splitlines())

#其他函数
#count ()函数统计字符串中指定字符出现的次数
print(str1.count("l"))
print(str1.count("or"))
#join()函数将字符串中的每个字符连接起来，返回一个字符串
#序列中的元素必须是字符串才能连接
list1=["hello","world","nihao"]
str2="_"
str3=" "
print(str2.join(list1))
print(str3.join(list1))
#replace()函数将字符串中的指定字符替换成另一个字符，返回一个新的字符串
#并且可以指定替换的次数
print(str1.replace("l","L"))
print(str1.replace("l","L",2))
#capitalize()函数将字符串的第一个字符转换成大写字母，其他字符转换成小写字母
print(str1.capitalize())
print(str1.title()) #title()是每个单词都给首字母大写