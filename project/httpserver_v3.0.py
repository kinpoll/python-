#coding=utf-8
'''
aid httpserver v3.0
'''
from socket import *
import sys
from threading import Thread
from settings import *#导入配置文件
import re

#和WebFrame通信
def connect_frame():
    s=socket()
    s.connect(frame_address)#连接框架服务器地址
    #####################################################################################################################


class HTTPServer(boject):
    def __init__(self,address):
        self.address=address
        self.create_socket()
        self.bind(address)
    def create_socket(self):
        self.sockfd=socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    def bind(self):
        self.ip=address[0]
        self.port=address[1]
        self.sockfd.bind(address)
    def serve_forever(self):
        self.sockfd.listen(5)
        print('Listen to port %d' % self.port)
        while True:
            try:
                connfd, addr = self.sockfd.accept()
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit('Server exit!')
            except Exception as e:
                print('Error:', e)
                continue
            print('connect from',addr)
            # Create threads to process client requests
            handle_client = Thread(target=self.handle, args=(connfd,))
            handle_client.setDaemon(True)
            handle_client.start() 
    def handle(self,connfd):
        #接收浏览器发来的http请求
        request=connfd.recv(4096)
        if not request:
            return
        request_lines=request.splitlines()    
        #获取请求行
        request_line=request_lines[0].decode('utf-8')
        pattern=r'(?P<METHOD>[A-Z]+)\s+(?P<PATH_INFO>/\S*)'
        try:
            env=re.match(pattern,request_line).groupdict()
        except:
            response='HTTP/1.1 500 SERVER ERROR\r\n'
            response+='\r\n'
            response+='Server Error'
            connfd.send(response.encode())
        
        





if __name__=="__main__":
    httpd=HTTPServer(ADDR)
    httpd.server_forever()