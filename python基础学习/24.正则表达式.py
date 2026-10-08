#正则表达式：用一个字符串去匹配另一个字符串，匹配的过程中，就需要去符合某一种语法规则
#通常用来检索、替换符合一个规则的文本
#1.配什么字符
#:匹配任意字符（换行符除外）
#\d匹配数字字符
#\D匹配非数字字符
#\w匹配单词字符（英文、数字、下划线）
#\W匹配非单词字符
#\s匹配空白符（包括换行符、tab、空格）
#\S匹配非空白字符
#2.匹配次数
#*出现0次或多次（贪婪）
#+出现1次或多次（贪婪）
#：出现0次或1次（懒惰）
#{n}：出现n次
#{n, m}：出现n~m次
#{n,}：出现n次以上
#3.匹配地方
#^：在行首的位置匹配
#$：在行尾的位置匹配
#\b：表示匹配单词边界。（比如\bword，可以匹配 word、words，但不会匹配 sword）
#4.匹配指定格式字符
#使用 () 匹配指定格式的字符，比如：
#(ab)：表示在文本中只匹配 ab 这两个字符，且必须相邻
#(a|b)：表示在文本中匹配 a 或者 b 这两个字符，不一定相邻。
#注意：( ) 会把匹配到的内容保存在内存上，开发者可以使用 \n 来代表一个匹配模式中第 n 个 () 中匹配到的内容。
#使用 [] 匹配指定类别的字符串，比如：
#[abcd]：表示匹配 a 或匹配 b 或匹配 c 或匹配 d
#[a-d]：表示匹配 a 或匹配 b 或匹配 c 或匹配 d
#[a-zA-Z0-9]：表示匹配所有的大小写英文和数字
#[^0-9]：表示匹配除了数字之外的所有字符 上三角表示取反
#5.单行、多行模式
#单行模式：在单行模式下，.可以匹配任何的字符，包括换行符，并且整个文本会被认为是一个完整的文本，使用 ^ 和 $ 只能匹配到文本的开头和结尾。
#多行模式：在多行模式下，.就不可以匹配换行符了，使用 ^ 和 $ 可以匹配到每一行的开始和结束。
#贪婪模式：在正则表达式中尽可能多的匹配字符
#懒惰模式：在正则表达式中尽可能少的匹配字符
#6.?的用法
#?作为限定符，表示修饰对象只能出现0次或1次
#?放在量词前，将匹配模式改为懒惰匹配模式
#(?=pattern)表示将匹配模式改为懒惰匹配模式
#(?!pattern)表示匹配位置后面不能跟着pattern模式的字符
#(?<=pattern)表示匹配位置前面必须跟着pattern模式的字符
#(?!pattern)表示匹配位置前面不能跟着pattern模式的字符
#(?:pattern)表示将pattern包含在一个分组中，但不将这个分组的匹配结果保存到分组编号中
text = '''
asfsafasfafs
1564551565
15646488322
13315561889


'''
import re
pattern = r"^[1]{1}[3589]{1}[0-9]{9}$"
res = re.search(pattern,text,re.M)
if res:
    print(res.group())
    print(res.start())  #字符起始位置

#findall函数：从文本中寻找所有与模式匹配的子串，并将所有匹配结果存储到列表中进行返回，匹配失败返回一个空列表
#使用方法：re.findall(pattern,string,flags=0)
#pattern：正则表达式的格式 string：被匹配的文本 flags：标志位，控制正则表达式的匹配方式，如：是否区分大小写，设置多行匹配模式
#应用场景：提取多个子串
res1 = re.findall(pattern,text,re.M)
print(res1)

#sub函数：将文本中与模式匹配的部分替换为其他的内容
#使用方法：re.sub(pattern,repl,string,count,flags=0)
#repl:替换文本或一个函数，若是文本，就将匹配到内容替换为该文本，若是函数，在函数中进行文本处理的操作
#count（可选）：替换的最大次数，默认值为0，表示替换所有匹配项
#应用场景：文本格式化、数据清洗、敏感信息脱敏
text1 = "2002.04.20"
pattern = r"(\d{4})\.(\d{2})\.(\d{2})"
replacement = r"\1年\2月\3日" #()会把匹配到的内容放在内存上，开发者可以使用\n代表一个匹配模式中第n个()中匹配到的内容
new_text = re.sub(pattern,replacement,text1)
print(new_text)
#使用函数替换
text2 = 'Hello 123 World 456'
pattern = r"\d+"  #定义正则表达式模式，匹配数字
#定义替换函数
def replace(match):
    number = int(match.group())
    return str(number*2)
new_text1 = re.sub(pattern,replace,text2)
print(new_text1)
#脱敏处理：
text3 = "身份证号:510042652222223461"
def desensitize_info(text):
    id_card_pattern = r"(\d{6})(\d{4})(\d{4})(\d{3})(\d|X)"
    text = re.sub(id_card_pattern,r'\1******\4\5',text)
    return text
desensitized_text = desensitize_info(text3)
print(desensitized_text)

#re.split函数：将文本根据匹配模式进行分割，将分割后的结果放入列表中进行返回
#使用方法：re.split(pattern,string,maxsplit,flags=0)
#maxsplit（可选）：表示最大分割次数，默认值为0，表示分割所有匹配项
text4="apple, banana, orange, watermelon"
pattern=r",\s*"
fruits = re.split(pattern,text4)  #分割成了一个一个单词，生成元组返回
print(fruits)  

#re.compile函数：预先编译正则表达式要匹配的模式，并返回一个正则表达式的对象，该对象与re.match返回的对象不同，该对象可调用上面的函数
#re.compile(pattern,flags=0)
#应用场景：多次匹配，在一个较长的文本中多次应用同一个正则表达式时，使用re.compile可避免每次匹配都重新编译表达式
email_pattern = re.compile(r"[1]{1}[3589]{1}[0-9]{9}")
emails = re.search(email_pattern,text)
print(emails.group())