from socket import *
import sys
import os

class Chatclient():
    def __init__(self,s):
        self.s=s
    def register(self):
        while True:
            dict={}
            dict['nickname']=input('请设置一个昵称:')
            dict['username']=input('填写您的真实姓名:')
            dict['password']=input('请设置您的密码')
            dict2=input('重输密码进行确认:')
            dict['sex']=input('选择性别：')
            dict['tel']=input('填写您的联系方式:')   
            if dict2==dict['password']:
                break
            else:
                print('两次密码输入不一致，请重新设置')
                continue 
        self.s.send(('R#{}'.format(dict)).encode())
        print(self.s.recv(40960).decode())


    def log(self):
        while True:
            account_id=int(input('账号:'))
            password=input('密码:')
            self.s.send(('L#{}#{}'.format(account_id,password)).encode())
            data=self.s.recv(40960).decode()
            if data=='登录成功':
                print(data)
                return 
            else:
                print(data,'请重新输入\n')
                continue


def main():
    if len(sys.argv)<3:
        return 
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    ADDR=(HOST,PORT)
    s=socket()
    try:
        s.connect(ADDR)
    except Exception as e:
        print('连接服务器失败:',e)
        return 
    chat=Chatclient(s)
    while True:
        print('---register---\n---log---\n')
        cmd=input('请输入选择功能:').strip()
        if cmd=='register':
            chat.register()
        if cmd=='log':
            chat.log()
            s.close()
            break







if __name__=='__main__':
    main()   
