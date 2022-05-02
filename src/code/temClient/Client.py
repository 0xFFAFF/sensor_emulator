# -*- coding: utf-8 -*-
'''
客户端发送数据并接受服务器端的控制信息
Created on 2022-04-18   12:10:21
@author: TA
'''
import os
import threading
import time
import re
import json
from socket import *
from queue import Queue

BUFSIZE = 1024  # 缓冲区大小
SEND_STATE = 1  # 处于发送状态
STOP_STATE = 0  # 处于停止状态
SEVRVER_IP = '127.0.0.1'  # 服务器IP
SERVER_PORT = 50000  # 服务器端口


class TemEmulator:
    def __init__(self):
        self.interval = 1
        self.stage = SEND_STATE

    def read_data_content(self):
        '''
        读取文件中模拟的整块温度数据
        '''
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'temperature.csv')
        with open(filename, 'r') as f:
            data = f.read()
        return data

    def org_data(self):
        '''
        组织温度数据，以便发送
        '''
        content = self.read_data_content()
        datalist = content.split('\n')
        return datalist

    def generate_date(self, queue):
        data = self.org_data()
        l = threading.Lock()
        for i in data:
            while self.stage == STOP_STATE:
                time.sleep(self.interval)
                continue
            print('1', type(i))
            
            ID = i.split(',')[0]
            sensor_data = i.split(',')[1]
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 获取当前时间
            item_raw = {'ID': ID, 'data_type': 'temprature', 'sensor_data': sensor_data, 'time': now_time}
            item = json.dumps(item_raw)
            
            l.acquire()
            queue.put(item)
            l.release()
            time.sleep(self.interval)

    def set_stage(self, stage):
        self.stage = stage
    
    def set_interval(self, interval):
        self.interval = interval

class Client():
    def __init__(self, serverIp, serverPort, TemEmulator):
        self.serverIp = serverIp
        self.serverPort = serverPort
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.TemEmulator = TemEmulator
        self.queue = Queue()  # 定义一个队列,用于存放接收到的传感器数据，用于发送
        self.serverQueue = Queue()  # 定义一个队列,用于存放接收到的服务器指令数据，用于接收

    def get_emulator_data(self):
        '''
        获取传感器数据的线程，间隔为interval秒
        '''
        getDataThread = threading.Thread(target=self.TemEmulator.generate_date, args=(self.queue,))
        getDataThread.start()

    def reveive_thread(self):
        while True:
            try:
                data = self.clientSocket.recv(BUFSIZE).decode('utf-8')
                self.serverQueue.put(data)
                self.parse()
            except ConnectionResetError:
                print('远程服务器已关闭，发送线程已自动退出')
                return
            
            except TimeoutError:
                print('接受超时，已自动退出')
                return

    def send_thread(self):
        while True:
            if(self.queue.empty()):
                continue
            data = self.queue.get()
            print('2', type(data))
            try:
                self.clientSocket.send(data.encode('utf-8'))
            except ConnectionResetError:
                print('远程服务器已关闭，接受线程已自动退出')
                break

    def communicate(self):
        try:
            self.clientSocket.connect((self.serverIp, self.serverPort))
            
        except ConnectionRefusedError:
            print('远程服务器未启动，传感器数据无法发送，已自动退出')
            return
        sendThread = threading.Thread(target=self.send_thread, args=())
        
        recvThread = threading.Thread(target=self.reveive_thread, args=())
        
        sendThread.start()
        recvThread.start()
        
        sendThread.join()
        recvThread.join()
        self.clientSocket.close()

    def get_queue(self):
        '''
        返回一个队列，存放接收到的传感器数据
        '''
        return self.queue

    def get_interval(self):
        return self.interval

    def parse(self):
        if self.serverQueue.empty():
            return
        raw_data = self.serverQueue.get()
        if raw_data == 'stop':
            self.TemEmulator.set_stage(STOP_STATE)
            print('正在设置stop状态')
        elif raw_data == 'start':
            self.TemEmulator.set_stage(SEND_STATE)
        elif re.match('interval [0-9]+', raw_data) != None:
            self.TemEmulator.set_interval(int(raw_data[8:]))





if __name__ == '__main__':
    emulator = TemEmulator()
    client = Client(SEVRVER_IP, SERVER_PORT, emulator)
    client.get_emulator_data()
    client.communicate()

    print('hello')
