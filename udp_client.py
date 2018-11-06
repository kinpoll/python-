import gevent
from gevent import monkey
monkey.patch_all()
from socket import *
import sys
import os


# 发送消息
def add_send(s, self_account_id):
    while True:
        account_id = input('请输入对方账号>>')
        text = 'A#%s#%s' % (account_id, self_account_id)
        s.sendto(text.encode(), ('176.234.96.87', 6666))
        data, addr = s.recvfrom(4096)
        dataList = data.decode().split('#')
        if dataList[0] == 'N':
            print('账号输入有误，请重新输入\n')
            continue
        if dataList[0] == 'yes':
            print('添加成功')
            break
        if dataList[0] == 'no':
            print('对方拒绝')
            break


# 接收消息
def reply_add(s):
    while True:
        data, addr = s.recvfrom(10240)
        print(data.decode())
        if data.decode().split('#')[1] == '请求加你为好友':
            print('\n%s' % data.decode())
            nickname = data.decode().split('#')[0]
            judge = input('yes or no>>')
            s.sendto(('R#%s#%s' % (judge, nickname)).encode(),
                     ('176.234.96.87', 6666))
            if judge == 'yes':
                print('\n您已同意添加对方为好友')
                break


def show_list(s):
    s.sendto('G#G#G'.encode(), ('176.234.96.87', 6666))
    data, addr = s.recvfrom(40960)
    print('好友列表:', eval(data.decode()))


def log(s):
    while True:
        account_id = input('账号:')
        password = input('密码:')
        s.sendto(('L#{}#{}'.format(account_id, password)
                  ).encode(), ('176.234.96.87', 6666))
        data, addr = s.recvfrom(40960)
        if data.decode() == '登录成功':
            print(data.decode())
            return account_id
        else:
            print(data.decode(), '请重新输入\n')
            continue


def main():
    s = socket(AF_INET, SOCK_DGRAM)
    while True:
        print('--log--\n--add--\n--receive--\n--list--\n')
        cmd = input('输入选项>>')
        if cmd == 'log':
            self_account_id = log(s)
        if cmd == 'add':
            add_send(s, self_account_id)
        if cmd == 'receive':
            reply_add(s)
        if cmd == 'list':
            show_list(s)


if __name__ == '__main__':
    main()


# | 122968811  | kinpoll  | 10 | 王泽宇    | 123456   | 男   | 13227737207 | ('176.234.96.87', 40041) |
# | 119646452  | lulu     | 11 | 璐璐      | 654321   | 女   | 18792916870 | ('176.234.96.87', 49186)
