# -*- coding: utf-8 -*-
'''
客户端发送数据并接受服务器端的控制信息
Created on 2022-04-18   12:10:21
@author: TA
'''
import threading
class Client():
    pass

class ClientThread(threading.Threas):
    def __init__(self, client):
        self.client = client
        threading.Thread.__init__(self)
        
    def run():
        pass