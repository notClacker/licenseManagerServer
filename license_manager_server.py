#!/usr/bin/env python3

import asyncore
import socket
import time

import cfg
from cfg import logger
import request_handler


class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        for attempt in range(cfg.g_max_attempts):
            try:
                data = self.recv(cfg.g_count_of_received_symbols)    
                logger.debug(data)
                response = request_handler.processingRequest(data)
                logger.debug(response)
                self.send(response + b'\0')                
            except Exception as err:
                logger.error(err)
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
            logger.debug('conn ' + str(addr))
            handler = EchoHandler(sock)


if __name__ == "__main__": 
    ## FAKE-UNIT TEST
    ## data = b'mo|1337-7331|deadbeaf'
    #data = b'mo|12|beefdea'
    #response = request_handler.processingRequest(data)
    #logger.debug(response)
    #exit(0)
    ## DELETE    

    while True:
        try:            
            logger.info("Server is started")
            server = EchoServer(cfg.HOST, cfg.PORT)
            asyncore.loop()

        except Exception as err:
            logger.error(err)
            time.sleep(cfg.g_error_sleep_sec)

