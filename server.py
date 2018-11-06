from socket import *
import sys,os
from multiprocessing import Process
from mysqlpython import *
from random import *

def register(c,dict):
    nickname=dict['nickname']
    username=dict['username']
    password=dict['password']
    sex=dict['sex']
    tel=dict['tel']
    account_id=str(randint(100000000,1000000000))
    sqlh = Mysqlpython('chatroom')
    sqlh.zhixing('insert into user(account_id,nickname,username,password,sex,tel) value(%s,%s,%s,%s,%s,%s)',[account_id,nickname,username,password,sex,tel])    
    c.send(('注册成功，您的账号为 %s'%account_id).encode())
    sel='create table l{}(id int primary key auto_increment,nickname varchar(30))charset=utf8'.format(account_id)
    sqlh.zhixing(sel)    


def log(c,dataList):
    while True:
        password = dataList[2]
        # 两个密码作对比
        sqlh = Mysqlpython('chatroom')
        sel = 'select password from user where account_id=%s'
        r = sqlh.get_select(sel, [dataList[1]])
        if len(r) == 0:
            c.send('用户名不存在'.encode())
        elif password == r[0][0]:
            c.send('登录成功'.encode())
            addr=str(c.getpeername())
            sqlh.zhixing('update user set addr=%s where account_id=%s',[addr,dataList[1]])
            c.close()  
            sys.exit(0) 
        else:
            c.send('密码错误'.encode())               


def handler(c,s):
    s.close()
    while True:
        data = c.recv(10240).decode()
        if not data:
            break
        # 收到一个字典键值对绑定注册字段--值'R dict'
        dataList=data.split('#')
        if dataList[0]=='R':
            register(c,eval(dataList[1]))
        if dataList[0]=='L':
            log(c,dataList)
    c.close()
    sys.exit(0)    


def main():
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(('0.0.0.0',8888))
    s.listen(10)
    while True:
        try:
            c,addr=s.accept()
        except KeyboardInterrupt:
            sys.exit('服务器退出')
        except Exception as e:
            print('报错:',e)
        p=Process(target=handler,args=(c,s,))    
        p.daemon=True
        p.start()
           

if __name__=='__main__':
    main()