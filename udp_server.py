from socket import *
import sys
import os
from multiprocessing import Process
from mysqlpython import *



def log(s, dataList, addr):
    while True:
        password = dataList[2]
        # 两个密码作对比
        sqlh = Mysqlpython('chatroom')
        sel = 'select password from user where account_id=%s'
        r = sqlh.get_select(sel, [dataList[1]])
        if len(r) == 0:
            s.sendto('用户名不存在'.encode(), addr)
            break
        elif password == r[0][0]:
            s.sendto('登录成功'.encode(), addr)
            sqlh.zhixing('update user set addr=%s where account_id=%s', [
                         str(addr), dataList[1]])
            return
        else:
            s.sendto('密码错误'.encode(), addr)
            break


def do_send(s, dataList, addr):
    sqlh = Mysqlpython('chatroom')
    sel1 = 'select nickname from user where account_id=%s'
    sel2 = 'select addr from user where account_id=%s'
    r1 = sqlh.get_select(sel1, [dataList[2]])
    r2 = sqlh.get_select(sel2, [dataList[1]])
    if r2 == ():
        s.sendto('N#N#N'.encode(), addr)
        return
    msg = '%s#请求加你为好友' % r1[0][0]
    ADDR = eval(r2[0][0])
    s.sendto(msg.encode(), ADDR)


def do_reply(s, dataList, addr):
    sqlh = Mysqlpython('chatroom')
    sel1 = 'select addr,account_id from user where nickname=%s'  # nickname是申请加好友端
    sel2 = 'select nickname,account_id from user where addr=%s'  # nickname是被申请端
    r1 = sqlh.get_select(sel1, [dataList[2]])
    r2 = sqlh.get_select(sel2, [str(addr)])
    print(r1[0][1], r2[0][0], r2[0][1], dataList[2])
    sel3 = 'insert into l{0}(nickname) values("{1}")'.format(
        r1[0][1], r2[0][0])
    sqlh.zhixing(sel3)
    sel4 = 'insert into l{0}(nickname) values("{1}")'.format(
        r2[0][1], dataList[2])
    sqlh.zhixing(sel4)
    ADDR = eval(r1[0][0])
    nickname = r2[0][0]
    msg = '%s#%s' % (dataList[1], nickname)
    s.sendto(msg.encode(), ADDR)


def do_getlist(s, addr):
    sqlh = Mysqlpython('chatroom')
    sel1 = 'select account_id from user where addr=%s'
    r1 = sqlh.get_select(sel1, [str(addr)])
    sel2 = 'select nickname from l{}'.format(r1[0][0])
    r2 = sqlh.get_select(sel2)
    List = []
    i = 0
    while i < len(r2):
        List.append(r2[i][0])
        i += 1
    s.sendto(str(List).encode(), addr)


def handler(s):
    while True:
        data, addr = s.recvfrom(10240)
        if not data:
            break
        # 收到一个字典键值对绑定注册字段--值'R dict'
        dataList = data.decode().split('#')
        if dataList[0] == 'L':
            log(s, dataList, addr)
            continue
        if dataList[0] == 'A':
            do_send(s, dataList, addr)
            continue
        if dataList[0] == 'R':
            do_reply(s, dataList, addr)
        if dataList[0] == 'G':
            do_getlist(s, addr)

    s.close()
    sys.exit(0)


def main():
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 6666))
    pid = os.fork()
    if pid < 0:
        print('创建进程失败')
    if pid == 0:
        msg = input('请输入管理员内容:\n')
        msg = 'C 管理员 '+msg
        s.sendto(msg.encode(), ADDR)
    else:
        # 用于接收各种用户端请求，调用相应的函数处理
        handler(s)


if __name__ == '__main__':
    main()
