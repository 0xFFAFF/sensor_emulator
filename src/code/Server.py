# -*- coding: utf-8 -*-
'''
Created on 2022-04-20   10:21:06
@author: TA
'''

from socket import *
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000
BUFFSIZE = 1024


class Server():
    def __init__(self, serverIp, serverPort):
        self.serverIp = serverIp
        self.serverPort = serverPort
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.serverIp, self.serverPort))
        self.serverSocket.listen(10)
    
    def communication(self):
        while True:
            clientSocket, clientAddr = self.serverSocket.accept()
            print('clientAddr:', clientAddr)
            while True:
                data = clientSocket.recv(BUFFSIZE)
                if data == 'exit':
                    break
                print('data:', data)
                clientSocket.send('hello'.encode('utf-8'))
            clientSocket.close()
        # self.clientSocket, self.clientAddr = self.serverSocket.accept()
        # self.clientSocket.settimeout(10)
        # self.data = self.clientSocket.recv(BUFSIZE)
        # self.clientSocket.send('hello'.encode('utf-8'))
        # self.clientSocket.recv(BUFSIZE)
        # self.clientSocket.send('exit'.encode('utf-8'))
        # self.clientSocket.close()
        # self.serverSocket.close()

if __name__ == '__main__':
    server = Server(SERVER_IP, SERVER_PORT)
    server.communication()
    