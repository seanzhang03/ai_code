import pymysql
import os
from dotenv import load_dotenv

load_dotenv()  #解析.env文件，然后将找到的所有变量作为环境变量加载，通过os.getenv(key)方法获取值

class LoadMySQLConn:
    def __init__(self):
        self.conn = self.load_mysql_conn()
        #由于定义了2次conn，要获取连接既可以使用LoadDatabaseConn().conn
        # 也可以使用LoadDatabaseConn().load_mysql_conn


    # 加载mysql连接
    @staticmethod
    def load_mysql_conn():
        return pymysql.connect(          #connect返回一个connection对象
            host='localhost',  # 数据库服务器的ip
            user='root' ,  # 连接账号
            password='18782344351',  # 连接密码 --- root账户对应的密码
            database='test',  # 操作的数据库名称
            charset='utf8mb4',  # 字符编码
            cursorclass=pymysql.cursors.DictCursor  # 查询结果以字典的格式返回
        )

    '''
    @staticmethod
    def load_mysql_conn():
        return pymysql.connect(  # connect返回一个connection对象
            host=os.getenv("MYSQL_HOST"),  # 数据库服务器的ip
            port = int(os.getenv("MYSQL_PORT")), #数据库服务器的端口
            user=os.getenv("MYSQL_USER"),  # 连接账号
            password=os.getenv("MYSQL_PASSWORD"),  # 连接密码 --- root账户对应的密码
            database=os.getenv("MYSQL_DATABASE"),  # 操作的数据库名称
            charset='utf8mb4',  # 字符编码
            cursorclass=pymysql.cursors.DictCursor  # 查询结果以字典的格式返回
        )
    '''

    #connection对象常用方法
    #cursor()创建游标
    #commit()提交事务
    #rollback()回滚事务
    #close()关闭连接


    # 关闭mysql连接
    @staticmethod
    def close_mysql_conn(cursor, conn):
        cursor.close()  #显示关闭游标，释放其关联资源
        conn.close()  #关闭与mysql数据库的连接，释放所有资源


#1、创建数据库连接
#2、创建操作数据库的对象---这个对象叫游标对象
#3、定义操作数据库的指令---SQL
#sql命令中，email=%s中，email就是表里的字段，=条件关系，%s占位符表示一个变量
#%s如果涉及多个，有顺序问题，后期执行sql的时候按照顺序依次传值
#4、执行sql
#cursor.execute(sql,["123456@qq.com"])
#execute：执行sql的方法，参数2个：
#1、必须有的，sql命令语句
#2、可选项，如果sql命令中存在参数，那么就需要写，否则可以不写
#注意事项：参数必须放在列表[元组、字典]里面
#5、获取查询操作的结果[这个步骤只有查询操作才有]
