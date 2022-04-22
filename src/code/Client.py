# -*- coding: utf-8 -*-
'''
客户端发送数据并接受服务器端的控制信息
Created on 2022-04-18   12:10:21
@author: TA
'''
import os
import threading
import time
from socket import *

BUFSIZE = 1024  # 缓冲区大小
SEND_STATE = 1  # 处于发送状态
STOP_STATE = 0  # 处于停止状态
SEVRVER_IP = '127.0.0.1'  # 服务器IP
SERVER_PORT = 50000  # 服务器端口


def read_emulator_data():
    '''
    读取模拟的温度数据
    '''
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'temperature.csv')
    with open(filename, 'r') as f:
        data = f.read()
    return data


def org_data():
    '''
    组织温度数据，以便发送
    '''
    content = read_emulator_data()
    datalist = content.split('\n')
    return datalist


class Client():
    def __init__(self, serverIp, serverPort):
        self.state = SEND_STATE
        self.serverIp = serverIp
        self.serverPort = serverPort
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.interval = 5
        # self.clientSocket.connect((self.serverIp, self.serverPort))
        # self.clientSocket.settimeout(10)
        # self.clientSocket.send('hello'.encode('utf-8'))
        # self.clientSocket.recv(1024)
        # self.clientSocket.send('exit'.encode('utf-8'))
        # self.clientSocket.close()

    def communicate(self, data):
        i = 0
        with self.clientSocket as s:
            s.connect((self.serverIp, self.serverPort))
            s.settimeout(10)
            while True:
                if self.state == SEND_STATE:
                    s.send(data[i].encode('utf-8'))
                    i = i+1
                    s.recv(BUFSIZE)
                    time.sleep(self.interval)
                elif self.state == STOP_STATE:
                    s.recv(BUFSIZE)
                    continue


class ClientThread(threading.Thread):
    def __init__(self, client):
        self.client = client
        threading.Thread.__init__(self)

    def run():
        pass


if __name__ == '__main__':
    data = org_data()
    client = Client(SEVRVER_IP, SERVER_PORT)
    client.communicate(data)

    print('hello')
