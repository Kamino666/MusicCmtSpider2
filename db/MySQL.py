from pymysql import *


class CmtsDB:
    db_conf = {}

    def __init__(self, host, user, pwd, database, port=3306, charset='utf8'):
        # 初始化连接和游标
        self.conn = connect(host=host, port=port, user=user, password=pwd, database=database, charset=charset)
        self.cursor = self.conn.cursor()

    def __del__(self):
        # 关闭链接
        self.cursor.close()
        self.conn.close()

    def pushsingle(self, table, params):
        """
        将一个数据执行上传的sql语句
        :param table:str
        :param params:tuple contains 5 params
        :return: bool
        """
        # 执行sql
        sql = "insert into " + table + "(content,username,userid,time,likes) values(%s,%s,%s,%s,%s);"
        self.cursor.execute(sql, params)
        self.conn.commit()

    pass
