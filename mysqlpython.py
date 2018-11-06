# coding=utf-8
'''
mysql交互类\n
env:python 3.5\n
mysql\n
'''


from pymysql import *
class Mysqlpython:
    def __init__(self, database, host='localhost', user='root', password='123456', charset='utf8', port=3306):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        self.port = port
    def open(self):
        self.db = connect(host=self.host, user=self.user, password=self.password,
                          database=self.database, charset=self.charset, port=self.port)
        self.cur = self.db.cursor()
    def close(self):
        self.cur.close()
        self.db.close()
    def zhixing(self, sql, L=[]):
        self.open()
        self.cur.execute(sql, L)
        self.db.commit()
        self.close()
    def get_select(self, sql, L=[]):
        self.open()
        self.cur.execute(sql,L)
        return self.cur.fetchall()
if __name__ =='__main__':
    sqlh = Mysqlpython('chatroom')
    a=sqlh.get_select('select username from user where password=987')
    print(a)