#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
import socket, time

ir = InfraredSensor('in1')
ir.mode = 'IR-PROX'

ir2 = InfraredSensor('in2')
ir2.mode = 'IR-PROX'

while True:
    try:
        while True:
            Servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Servidor.connect(('169.255.168.150', 3550))

            Str_Env = "%d,%d" %(ir.value(), ir2.value())
            St = Str_Env.encode('utf-8')

            Servidor.send(St)

        Servidor.close()
    except Exception as e:
        print(e)
        time.sleep(1)