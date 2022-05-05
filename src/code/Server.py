# -*- coding: utf-8 -*-
'''
Created on 2022-04-20   10:21:06
@author: TA
'''

from socket import *
from queue import Queue
import threading
import re
import pymongo
import json
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000
BUFFSIZE = 1024
conn_pool = [] #socket连接池

sendqueue = Queue()

'''
receive_thread()为服务器的发送函数，为了解决input输入导致的线程阻塞，无法接受数据问题。

args:
    clientSocket: 与客户端通信的数据socket
    clientAddr: 客户端的地址
    recvQueue: 接收队列，把接受到的数据放到这个队列中
'''
def receive_thread(clientSocket,clientAddr,database):
    collect = database['{}:{}'.format(clientAddr[0],clientAddr[1])]
    
    while True:
        try:
            data = json.loads(clientSocket.recv(BUFFSIZE).decode('utf-8'))
            collect.insert_one(data)
            # print('clientAddr:{clientAddr},Data:{data}'.format(clientAddr=clientAddr,data=data))
        except ConnectionResetError:
            print('Client {} 关闭了连接,接受线程已退出'.format(clientAddr))
            clientSocket.close()
            return
        # `recvQueue.put(data)

    

                
class Server():
    def __init__(self, serverIp, serverPort):
        self.serverIp = serverIp
        self.serverPort = serverPort
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.serverIp, self.serverPort))
        self.serverSocket.listen(10)
        self.client = pymongo.MongoClient(host='localhost', port=27017) 
        self.db = self.client['sensor_data']
        
    def accept(self):
        while True:
            clientSocket, clientAddr = self.serverSocket.accept()
            # clientSocket.settimeout(60)
            conn_pool.append(clientSocket)
            
            clientThread = threading.Thread(target=self.communication,args=(clientSocket,clientAddr,))
            clientThread.start()
    
    def communication(self,clientSocket,clientAddr):

        
        recvThread = threading.Thread(target=receive_thread,args=(clientSocket,clientAddr,self.db,))
        # sendThread = threading.Thread(target=send_thread,args=(clientSocket,clientAddr,))
        recvThread.start()
        # sendThread.start()
        
        recvThread.join()
        # sendThread.join()
        
        clientSocket.close()
        conn_pool.remove(clientSocket)


    def ui(self):
        while True:
                info = input('请输入要发送的信息：\n\
                                1.stop --传感器停止发送数据\n\
                                2.start --传感器开始发送数据\n\
                                3.interval {n} --设置传感器的发送间隔为n秒\n\
                                4.real time --获取实时数据\n');
                if (info != 'stop') & (info != 'start') & (re.match('interval [0-9]+',info)==None):
                    print('信息格式有误，请重新输入\n')
                    continue
                print('当前在线客户端为：')
                if(len(conn_pool)==0):
                    print('当前没有客户端在线\n')
                    continue
                for index,clientSocket in enumerate(iterable=conn_pool):
                    print('ID:{},地址为：{}'.format(index,clientSocket.getpeername()))
                    
                choose_client = input('输入信息要送往的客户端ID\n')
                for index,clientSocket in enumerate(iterable=conn_pool):
                    if index == int(choose_client):
                        try:
                            clientSocket.send(info.encode('utf-8'))
                            print('信息已经发送')
                            print('目的地址：{}'.format(clientSocket.getpeername()))
                            break
                        except ConnectionResetError:
                            print('Client {} 关闭了连接,发送线程已退出'.format(clientAddr))
                            break
                        except TimeoutError:
                            print('发送超时')
                            break
                
        
        
    def run(self):
        uiThread = threading.Thread(target=self.ui)
        acceptThread = threading.Thread(target=self.accept)
        uiThread.start()
        acceptThread.start()
        acceptThread.join()

     

    
if __name__ == '__main__':
    
    server = Server(SERVER_IP, SERVER_PORT)
    server.run()
       
    print('hello')
    