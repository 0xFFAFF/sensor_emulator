# -*- coding: utf-8 -*-
'''
Created on 2022-04-18   11:41:45
@author: TA
'''
import threading
import time
import re
from queue import Queue
host = '127.0.0.1'
data = 'hello world'
# port = 8888
# ADDR = (host, port)
# def thread1():
#         print('Thread1 is running...')
#         for i in range(10):
#             time.sleep(0.1)
#         print('Thread1 is ended.')

# def thread2():
#     print('Thread2 is running...')
#     print('Thread2 is ended.')   


# thread1 = threading.Thread(target=thread1)
# thread2 = threading.Thread(target=thread2)
# thread1.start()
# thread2.start()
# # thread1.join()

# print('Main thread is ended.')
# print('host:{host},Data:{data}'.format(host=host,data=data))


# class test:
#     def __init__(self):
#         self.a = 1
        
#     def get_a(self):
#         return self.a
    

# if __name__ == '__main__':
#     t = test()
#     a = t.get_a()
#     print(a)
#     a = 2
#     print(test().get_a())

# q = Queue()
# q.put('hello')
# print(type(q.get()))

# res = re.match('hello', 'hello world')
# print(res=='hello')

# while True:
#     info = input('请输入要发送的信息：\n1.stop --传感器停止发送数据\n2.start --传感器开始发送数据\
#                 \n3.interval {n} --设置传感器的发送间隔为n秒\n');
            
#     if (info != 'stop') & (info != 'start') & (re.match('interval [0-9]+',info)==None):
#         print('信息格式有误，请重新输入\n')


data = 'interval 5'
print(int(data[8:]))