#!/usr/bin/env python3

import asyncore
import socket
import time

import cfg
import request_handler

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        for attempt in range(cfg.g_max_attempts):
            try:
                data = self.recv(4096)
                #if data == b"close" or data == b"close\n":
                #    self.close()      
                response = request_handler.processingRequest(data)
                print(response)
                self.send(response + b'\0')                
            except Exception:
                time.sleep(cfg.g_error_sleep_sec)
            else:
                break


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


if __name__ == "__main__": 
    # FAKE-UNIT TEST
    # data = b'mo|1337-7331|deadbeaf'
    data = b'mo|1337-7331|1234-5678'
    response = request_handler.processingRequest(data)
    print(response)
    exit(0)
    # DELETE

    while True:
        # time.sleep(0.1)
        try:
            print("Started")
            server = EchoServer(cfg.HOST, cfg.PORT)
            asyncore.loop()

        except Exception as err:
            print("Exception!!!")
            logData = str(time.localtime())
            logData += "| Exception!!! | "
            logData += str(err)
            with open("log.txt", 'a') as logFile:
                logFile.write(logData + '\n')
            time.sleep(cfg.g_error_sleep_sec)

