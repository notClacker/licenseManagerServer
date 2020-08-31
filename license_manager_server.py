#!/usr/bin/env python3

import asyncore
import socket
import time

HOST = '0.0.0.0'
PORT = 2222

main_offset = 0x13377331

def processingRequest(request):
    response = request
    #tmp = bytes(request, 'utf-8')
    #splitedRequest = tmp.split('|')
    # if len(splitedRequest) > 1:
    #     requestType = splitedRequest[0]
    #     requestValue = splitedRequest[1]
    #     if requestType == b'mo':
    #         response = str(main_offset)

    return response

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(4096)
        if data == b"close" or data == b"close\n":
            self.close()
        # if data == b"restart\n":
        #     logData = str(time.localtime())
        #     logData += "| Exception!!! | "
        #     logData += Exception
        #     with open("log.txt", 'a') as logFile:
        #         logFile.write(logData + '\n')
        #     raise
        response = processingRequest(data)
        print(response)
        self.send(response + b'\0')

class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(11)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('conn', addr)
            handler = EchoHandler(sock)

while True:
    time.sleep(0.1)
    try:
        print("Started")
        server = EchoServer(HOST, PORT)
        asyncore.loop()

    except Exception:
        print("Exception!!!")
        logData = str(time.localtime())
        logData += "| Exception!!! | "
        logData += str(Exception)
        with open("log.txt", 'a') as logFile:
            logFile.write(logData + '\n')
