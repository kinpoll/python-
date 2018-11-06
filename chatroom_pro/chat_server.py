# coding=utf-8
'''
Chatroom
env:python 3.5
socket and fork
'''
from socket import *
import os
import sys
from time import *
t='%d:%d:%d'%localtime()[3:6]


def do_login(s, user, name, addr):
    if (name in user) or name == '管理员':
        s.sendto('该用户已存在'.encode(), addr)
        return
    s.sendto('OK'.encode(), addr)
    # 通知其他人
    msg = '\n--------------------------欢迎%s进入聊天室--------------------------' % name
    for i in user:
        s.sendto(msg.encode(), user[i])
    # 将用户加入字典
    user[name] = addr


def do_send(s, name, msg, user):
    msg = '\n\t\t\t\t%s发言:%s---(%s)' % (name, msg,t)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])


def do_quit(s, user, name):
    msg = '\n--------------------------%s退出了聊天室--------------------------' % name
    for i in user:
        if i == name:
            s.sendto('QUIT'.encode(), user[i])
        else:
            s.sendto(msg.encode(), user[i])
    # 从字典中删除用户
    del user[name]


def do_request(s):
    # 存储结构{'张三':('127.0.0.1',8888)}
    user = {}
    while True:
        msg, addr = s.recvfrom(10240)
        msgList = msg.decode().split(' ')
        # 区分请求类型
        if msgList[0] == 'L':
            do_login(s, user, msgList[1], addr)
        if msgList[0] == 'C':
            do_send(s, msgList[1], msgList[2], user)
        if msgList[0] == 'Q':
            do_quit(s, user, msgList[1])


# 创建网络连接
def main():
    ADDR = (('0.0.0.0', 8888))
    # 创建套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        print('创建进程失败')
    if pid == 0:
        msg = input('请输入管理员内容:')
        msg = 'C 管理员 '+msg
        s.sendto(msg.encode(), ADDR)
    else:
        # 用于接收各种用户端请求，调用相应的函数处理
        do_request(s)


if __name__ == '__main__':
    main()
