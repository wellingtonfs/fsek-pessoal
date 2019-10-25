#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import socket, time, json, math

uc = UltrasonicSensor('in1')
uc.mode = 'US-DIST-CM'

uf = UltrasonicSensor('in2')
uf.mode = 'US-DIST-CM'

ir = InfraredSensor('in3')
ir.mode = 'IR-PROX'

ut = UltrasonicSensor('in4')
ut.mode = 'US-DIST-CM'

class Communication(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(('169.255.168.150', 3572))
                
                    while True:

                        Sedex = {
                            "uc" : int(uc.value()),
                            "uf" : int(uf.value()),
                            "ir" : int(ir.value()),
                            "ut" : int(ut.value())
                        }

                        s.send(json.dumps(Sedex).encode())
                        #time.sleep(0.1)
                        
            except Exception as e:
                print(e)
                s.close()
                time.sleep(0.5)

comm = Communication()
comm.daemon = True
comm.start()

while True:
    pass