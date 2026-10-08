#文件由以下几部分组成：
#数据：文件中存储的实际信息，即用户想要保存的具体信息，如文本、图像或代码
#元数据：关于文件本身的附加信息，包括但不限于文件名、创建日期、大小、类型。用来描述文件本身的属性
#文件系统：os用来组织和管理文件的一种逻辑结构，包括文件的命名、存储和检索方式。文件系统还负责管理磁盘空间的分配，并确保文件可以给正常地读写
#文件属性：文件名（主文件名和扩展名）、位置、文件大小文件类型、创建日期和时间、修改日期和时间、访问权限
#open()函数来打开文件，该函数返回一个文件对象，用来后续的读写操作
#使用方法res = open(file_name,mode='r',buffering=None,encoding=None,errors=None,newline=None)
#参数说明
#file_name	要打开的文件的路径加名称（包含后缀名），可以是绝对路径或相对路径。
#mode	打开文件的模式，默认为 'r'，表示只读模式且以文本模式读取。
#buffering	可选参数，缓冲区大小。0 = 无缓冲1 = 行缓冲更大的整数 = 具体缓冲区大小,默认为 None，表示使用默认缓冲策略（大多数情况用默认值即可）。
#encoding	可选参数，用于指定文件的编码，仅适用于文本模式。默认为 None，表示使用系统的默认编码。
#errors	可选参数，用于指定如何处理编码和解码错误，对二进制模式无效。常见取值：'strict'、'ignore'、'replace' 等。
#newline	可选参数，用于控制通用换行符模式的行为。
#• None：启用通用换行符模式，'\n' 和 '\r\n' 都被识别为换行符，读取时转换为 '\n'
#• 其他值（如 '\n'、'\r'、'\r\n' 或 ''）：在该值处进行换行符转换。
#closefd
path = './1.txt'
#res = open('./2.txt','r')
'''
print(res)

#文件打开模式
#'r'：只读模式，文件不存在会触发异常
#'r+'：打开文件进行读写，文件必须存在
#'w'：写入模式，如果文件存在则覆盖，不存在就创建
#'w+'：打开文件进行读写，如果文件存在则覆盖，不存在就创建
#'a'：追加模式，如果文件存在则在末尾追加，不存在则创建
#'a+'：打开文件进行读写，如果文件存在则在末尾追加，不存在则创建，这种模式读取可能出错，因为是在上一次末尾位置进行读取
#'x'：独占创建模式，若文件已存在，则抛出异常，用来避免覆盖现有文件
#'b'：二进制模式，读写时，数据不会被转换，直接以字节形式处理
#'t'：读写时，数据会被视为字符串

#读取文件的内容
#read(size)：size为可选参数，文本模式下，一次最多读取文件指针后面size个字符，二进制模式则一次最多读取文件指针后面size个大小的字节
#默认size为None，表示一次性读取文件指针后面的所有内容并将其作为字符串返回
read_str = res.read()
print(read_str)
#readline()从文件中读取单行数据
#readlines()从文件中读取所有行数据，并返回一个列表
read_str1=res.readline()  #用'r'指针移到末尾了故不会读取到内容
read_str2=res.readlines()
print(read_str1)
print(read_str2)
'''
#写入文件
#write(str)：将str的内容覆盖到当前文件指针位置的后面，并将文件指针移动到新的写入位置。返回写入字符的数量
#写入其他类型的对象时，要将他们转换为字符串或字节对象   
res1 = open('./2.txt','rb+')
read_str3 = res1.read(3)  #在r+模式由于read为了效率，会一次性把一大块文件读入python内存缓冲区，所以在这种模式下写入可能会导致原本在中间的字符跳到末尾去写入
res1.write(b"nihao")  
print(res1.tell())

res1.close()

#文件关闭 功能：释放资源，刷新缓冲区，禁止进一步操作
#with语句：上下文管理器，来简化资源打开和关闭过程，确保资源在不需要时得到释放
#语法 with expression [as variable]
#         with-block
#表达式：这个表达式必须返回一个实现了上下文管理器协议的对象，也就是说，他需要包含__enter__和__exit__两个方法
#as子句：可选，如果提供了as子句，那么expession中__enter__方法的返回值将被赋值给变量
#with-block：该代码块是with语句的主体，在执行这个代码块之前，会首先调用上下文管理器的__enter__方法。
#当with-block执行完毕后，无论是因为正常完成还是因为异常，都会调用上下文管理器的__exit__方法，负责关闭文件
with open("./2.txt",'r') as fd:
    fd.close()

#文件指针操作
#tell()函数没有参数，功能就是返回文件指针当前位置相对于文件开头的偏移量，这个偏移量是一个整数
#表示从文件开头到当前读取位置的字节数
#该函数仅在文件被打开用于读取时才有意义，因为在写入模式下，文件指针的操作会随着写入操作而改变
#在读取模式下，tell返回的是当前读取位置相对于文件开头的偏移量
#其返回值是字节而非字符数，对utf-8编码来说，一个汉字占三字节，故读取中文时，字符和字节结果不一样

#用seek函数改变文件指针的位置
#seek(offset,whence=0)
#offset表示相对于whence的偏移量，是一个整数，偏移量为正数表示向文件末尾方向移动，负数表示向文件开头方向移动，0表示不偏移
#whence是可选参数，默认为0，0表示从文件开头开始计算偏移量，1表示从当前文件指针位置开始计算偏移量，2表示从文件末尾开始计算偏移量
with open("./2.txt",'r+') as fd:
    print(fd.tell())
    fd.seek(4)
    print(fd.tell())

import os
import time
print(os.path.getsize('./2.txt')) #获取文件大小
print(os.path.getmtime('./2.txt')) #获取最近修改时间
last_time = os.path.getmtime('./2.txt')
format = "%Y - %m - %d - %H : %M : %S"
lc_time = time.localtime(last_time)
res2 = time.strftime(format,lc_time)
print(res2)

#创建目录
#os.mkdir(path,mode=0o777)，path为要创建的目录的路径
#如果目录创建成功，则函数不返回任何内容，如果指定的路径已经存在就抛出异常，如果路径无效或权限不足无法创建目录则抛出异常
#os.mkdir只能创建一级目录，若父目录不存在，则抛出异常
#如果要创建多级目录，使用os.makedirs函数，会递归创建所需的中间目录
#os.mkdir('./test1')
#os.makedirs('./test2/test3')

#删除目录：在python中使用os.rmdir(path)来删除目录,这个函数删除时目录必须要为空目录
#os.rmdir('./test1')
print(os.getcwd())  #获取当前的工作目录
os.chdir('./test2')  #用来切换目录，若路径不存在或指定的为非目录就会抛出异常，切换成功什么都不返回
print(os.getcwd())
print(os.listdir('./'))  #用来获取指定目录下所有文件和子目录名称
print(os.path.isdir('./1.txt'))  #true表示是目录，false表示不是
os.chdir('../')
print(os.path.exists('./26.文件操作.py'))
print(os.path.isfile('./26.文件操作.py'))
#os.path.join(path, *paths)
#path是起始路径，通常为目录路径，paths为可变参数，需要连接到path的其他路径片段，返回一个字符串，表示将所有路径片段链接后的完整路径
#能确保生成的路径在不同os上是正确的，从而提高代码的可移植性，能避免手动拼接路径出现的错误，如忘记添加分隔符或添加错误分隔符
path='./'
ls = os.listdir(path)
print(ls)
new_ls = []
for name in ls:
    new_ls.append(os.path.join(path,name))  #把./全部添加到文件名前了
    print(new_ls)
print(os.path.abspath(path)) #绝对路径
#路径拆分
p,name = os.path.split(path)
print(p,name)