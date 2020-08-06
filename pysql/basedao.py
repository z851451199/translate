import pymysql
# #封装数据库访问基本类

class BaseDao():

    def __init__(self,host = '127.0.0.1',user = 'root',password = 'root',
                 database = 'dress',port = 3306,charset = 'utf8'):
        self.__connection = None  #定义连接对象，初始化None
        self.__cursor = None
        #定义配置参数
        self.__config = {'host' : host,'user' : user,'password' : password,
                 'database' :  database ,'port' : port,'charset' : charset}
    #封装获得数据库连接的方法
    def getConnection(self):

        if self.__connection != None:  #如果有连接对象，直接返回
            return self.__connection
            pass
        else:
            try:
                self.__connection = pymysql.connect(** self.__config)  #技巧 捕获异常
                return  self.__connection
            except Exception as e:
                print(e)
                pass
        pass

    def execute (self,sql,params = None):
        '''
        #用于执行数据库操作的方法，通用的方法
        :param sql: 需要执行的sql语句
        :param params: 需要传入的参数列表
        :return: 返回执行后的结果 int
        '''
        result  = 0
        try:
            self.__cursor = self.getConnection().cursor(cursor=pymysql.cursors.DictCursor) #获得游标
            if params:#params == Ture
                result = self.__cursor.execute(sql,params)
                pass
            else:
                result = self.__cursor.execute(sql, params)
                pass
        except Exception as e:
            print(e)
            pass
        return  result
        pass
    def commit(self):
        if self.__connection:
            self.__connection.commit()
        pass
    def rollback (self):#回滚
        if self.__connection:
            self.__connection.rollback()
            pass

    def close(self):#结束释放资源
        if self.__connection:
            self.__connection.close()
        pass
    def fetch (self):
        return self.__cursor.fetchall()
        pass
    pass