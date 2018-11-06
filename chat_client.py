from socket import *
import os
import sys


# 发送消息
def send_msg(s, name, addr):
    while True:
        text = input()
        if text == 'quit':
            text = 'Q '+name
            s.sendto(text.encode(), addr)
            sys.exit(0)
        text = 'C %s %s' % (name, text)
        s.sendto(text.encode(), addr)


# 接收消息
def recv_msg(s):
    while True:
        data, addr = s.recvfrom(10240)
        if data.decode() == 'QUIT':
            sys.exit('--------------------------您已退出！-------------------------')
        print(data.decode())


# 创建套接字
def main():
    # 从命令行输入服务器地址
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)

    # 创建套接字
    s = socket(AF_INET, SOCK_DGRAM)

    while True:
        name = input('输入姓名:')
        msg = 'L '+name
        # 发送给服务端
        s.sendto(msg.encode(), ADDR)
        # 等待回应
        data, addr = s.recvfrom(10240)
        if data.decode() == 'OK':
            print('--------------------------您已进入聊天室-------------------------')
            break
        else:
            print(data.decode())

    # 创建父子进程
    pid = os.fork()
    if pid < 0:
        sys.exit('创建进程失败')
    elif pid == 0:
        send_msg(s, name, ADDR)
    else:
        recv_msg(s)


if __name__ == '__main__':
    main()
