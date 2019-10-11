#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import socket, time

class Communication(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        cont = 0
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(('169.255.168.150', 3562))
                    
                    while True:
                        string = "%d" %cont
                        s.send(string.encode())
                        time.sleep(0.1)
                        cont += 1
            except Exception as e:
                print(e)
                s.close()
                time.sleep(0.5)

comm = Communication()
comm.daemon = True
comm.start()

while True:
    pass
        