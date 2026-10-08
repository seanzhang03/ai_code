#在python中，记录日志使用logging库，日志的级别从高到低为：
#1.CRITICAL：系统崩溃级别的错误，必须立即处理
#2.ERROR：运行时的错误，可能导致程序无法正常执行
#3.WARNING：警告信息
#4.INFO：信息性消息，程序正常运行
#5.DEBUG：详细信息，通常在诊断问题时有用
'''
import logging
#logging.basicConfig(level=logging.DEBUG) 通过设置权限来展示所有日志信息  #注：basicCoinfig只能调用一次，且要在其他日志操作前调用
logging.critical("这是一个critical信息")
logging.error("这是一个error信息")
logging.debug("这是一个debug信息")  #权限问题
logging.info("这是一个info信息")  #权限问题
logging.warning("这是一个警告信息")
'''

'''
import logging
#向指定的日志文件里去打印日志信息
logging.basicConfig(filename='./app.log',level=logging.DEBUG,filemode = 'a',format = "%(name)s - %(levelname)s - %(message)s")#a代表追加，w代表覆盖
#name：日志记录器名字 levelname：触发的种类比如warning message：指定的消息 asctime：时间
logging.warning("This is a warning message!")
'''

#创建自己的日志处理器
import logging
logger = logging.getLogger('mylogger')
logging.basicConfig(filename='./app.log',level=logging.DEBUG,filemode = 'w',format = "%(name)s - %(levelname)s - %(message)s")
logger.warning("这是我自己定义的日志处理器所记录的日志")