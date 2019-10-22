#!/usr/bin/env python3
from ev3dev.ev3 import *
from threading import *
import time, socket, json, math

class Communication(Thread):
    def __init__(self):
        self.sc_value = 0
        self.sc2_value = 0
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(('169.255.168.150', 3571))
                    s.listen()
                    while True:
                        conn, addr = s.accept()
                        with conn:
                            while True:
                                data = conn.recv(1024)

                                if not data:
                                    break

                                Sedex = json.loads(data.decode())
                                self.sc_value = Sedex['sc']
                                self.sc2_value = Sedex['sc2']
                                print(self.sc_value)

            except Exception as e:
                print(e)
                time.sleep(0.5)
    
Comm = Communication()
Comm.daemon = True
Comm.start()

while True:
    pass