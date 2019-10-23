#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import socket, time, json, math

Sensor_Cor = [ColorSensor('in1'), ColorSensor('in2')] #1 = Esquerdo, 2 = Direito
Sensor_Cor[0].mode = 'COL-COLOR'
Sensor_Cor[1].mode = 'COL-COLOR'

us = UltrasonicSensor('in3')
us.mode = 'US-DIST-CM'

us2 = UltrasonicSensor('in4')
us2.mode = 'US-DIST-CM'

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
                            "sc" : int(Sensor_Cor[0].value()),
                            "sc2" : int(Sensor_Cor[1].value()),
                            "us" : int(us.value()),
                            "us2" : int(us2.value())
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