#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
import socket, time
import math

ir = InfraredSensor('in1')
ir.mode = 'IR-PROX'

ir2 = InfraredSensor('in2')
ir2.mode = 'IR-PROX'

while True:
    try:
        while True:
            a = ir.value()
            b = ir2.value()

            if a > 99 or b > 99:
                continue

            Servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Servidor.connect(('169.255.168.150', 3550))

            print("%d --- %d" %ir.value() %ir2.value())

            Str_Env = "%d,%d" %(ir.value(), ir2.value())
            St = Str_Env.encode('utf-8')

            Servidor.send(St)
            Servidor.close()
            
            time.sleep(0.01)

            
    except Exception as e:
        print(e)
        time.sleep(1)
        