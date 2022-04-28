# -*- coding: utf-8 -*-
'''
Created on 2022-04-20   10:21:06
@author: TA
'''

from socket import *
from queue import Queue
import threading
import re


SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000
BUFFSIZE = 1024


'''
receive_thread()为服务器的发送函数，为了解决input输入导致的线程阻塞，无法接受数据问题。

args:
    clientSocket: 与客户端通信的数据socket
    clientAddr: 客户端的地址
    recvQueue: 接收队列，把接受到的数据放到这个队列中
'''
def receive_thread(clientSocket,clientAddr,recvQueue):
    while True:
        data = clientSocket.recv(BUFFSIZE).decode('utf-8')
       # print('clientAddr:{clientAddr},Data:{data}'.format(clientAddr=clientAddr,data=data))
        if data == 'exit':
            break
        recvQueue.put(data)


def send_thread(clientSocket):
    while True:
        info = input('请输入要发送的信息：\n1.stop --传感器停止发送数据\n2.start --传感器开始发送数据\
            \n3.interval {n} --设置传感器的发送间隔为n秒\n');
        
        if (info != 'stop') & (info != 'start') & (re.match('interval [0-9]+',info)==None):
            print('信息格式有误，请重新输入\n')
            continue
        clientSocket.send(info.encode('utf-8'))
        print('信息已经发送')
    

class Server():
    def __init__(self, serverIp, serverPort):
        self.serverIp = serverIp
        self.serverPort = serverPort
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.serverIp, self.serverPort))
        self.serverSocket.listen(10)
    
    def communication(self):
        q = Queue() # 用于存放接受到的数据
        
        clientSocket, clientAddr = self.serverSocket.accept()
        clientSocket.settimeout(60)
        recvThread = threading.Thread(target=receive_thread,args=(clientSocket,clientAddr,q,))
        sendThread = threading.Thread(target=send_thread,args=(clientSocket,))
        recvThread.start()
        sendThread.start()
        
        recvThread.join()
        sendThread.join()
        
        clientSocket.close()
        self.serverSocket.close()

if __name__ == '__main__':
    server = Server(SERVER_IP, SERVER_PORT)
    server.communication()
    