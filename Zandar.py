#!/usr/bin/env python3
from ev3dev.ev3 import *
from threading import *
import time, socket, json, math

class Communication(Thread):
    def __init__(self):
        self.ir_value = 0
        self.ir2_value = 0
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(('169.255.168.151', 3562))
                    s.listen()
                    while True:
                        conn, addr = s.accept()
                        with conn:
                            #print('Connected by', addr)
                            while True:
                                data = conn.recv(1024)

                                if not data:
                                    break

                                Sedex = json.loads(data.decode())
                                print(Sedex['IR1'])
            except Exception as e:
                print(e)
                time.sleep(0.5)
        

Comm = Communication()
Comm.daemon = True
Comm.start()

def Angulo_Reta(pontos):
    metade = int(len(pontos) / 2)
    media = [0, 0]
    for i in range(0, metade):
        media[0] += pontos[i]
        media[1] += 1

    ponto1 = int(media[0] / media[1])

    media = [0, 0]
    for i in range(metade, len(pontos)):
        media[0] += pontos[i]
        media[1] += 1

    ponto2 = int(media[0] / media[1])

    m = (ponto2 - ponto1) / (2)
    angulo = math.atan(m)
    print((angulo*57.2958))
    time.sleep(10)

while True:
    pass