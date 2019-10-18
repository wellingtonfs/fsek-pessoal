#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import socket, time, json
import math

ir = InfraredSensor('in1')
ir.mode = 'IR-PROX'

ir2 = InfraredSensor('in2')
ir2.mode = 'IR-PROX'

gy = GyroSensor('in3')
gy.mode = 'GYRO-ANG'

us = UltrassonicSensor('in4')
us.mode = 'US-DIST-CM'

class Communication(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(('169.255.168.150', 3563))
                
                    while True:

                        Sedex = {
                            "IR1" : ir.value(),
                            "IR2" : ir2.value(),
                            "GY" : gy.value(),
                            "US" : us.value()
                        }

                        s.send(json.dumps(Sedex).encode())
                        time.sleep(0.3)
            except Exception as e:
                print(e)
                s.close()
                time.sleep(0.5)

comm = Communication()
comm.daemon = True
comm.start()

while True:
    pass

        