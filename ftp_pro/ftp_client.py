from socket import *
import sys
import os
import time

# 将具体功能实现放在类中


class FtpClient():
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b'L')
        # 等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            data = self.sockfd.recv(4096).decode()
            files = data.split('#')
            for file in files:
                print(file, end=' ')
            print('\n文件列表展示结束')
        else:
            # 无法执行操作的原因
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit('客户端退出')

    def do_get(self, filename):
        self.sockfd.send(('G '+filename).encode())
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            fd = open(filename, 'wb')
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
            print('%s下载完毕\n' % filename)
        else:
            print(data)

    def do_put(self, filename):
        self.sockfd.send(('P '+filename).encode())

        try:
            fd = open(filename, 'rb')
        except:
            print('文件不存在')
            return
        while True:
            data = fd.read(1024)
            if not data:
                time.sleep(0.1)
                self.sockfd.send(b'##')
                break
            self.sockfd.send(data)
        fd.close()
        print(self.sockfd.recv(1024).decode())


# 网络连接
def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)

    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print('连接服务器失败：', e)
        return

    # 创建对象
    ftp = FtpClient(sockfd)

    while True:
        print('\n=============order options==========')
        print('              >>list                ')
        print('              >>get file            ')
        print('              >>put file            ')
        print('              >>quit                ')
        print('====================================\n')
        cmd = input('输入命令>>')
        if cmd.strip() == 'list':
            ftp.do_list()

        elif cmd.strip() == 'quit':
            ftp.do_quit()

        elif cmd[:3] == 'get':
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.split(' ')[-1]
            ftp.do_put(filename)
        else:
            print('请输入正确命令')


if __name__ == '__main__':
    main()
