#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
import socket, time

giro = GyroSensor('in1')
giro.mode='GYRO-ANG'

TC2 = TouchSensor('in4')

while True:
    try:
        while True:
            Servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Servidor.connect(('169.255.168.150', 3549))
            Str_Env = "%d," %giro.value()
            if TC2.value():
                Str_Env += "True"
            else:
                Str_Env += "False"
            St = Str_Env.encode('utf-8')
            Servidor.send(St)
            time.sleep(1)

        Servidor.close()
    except Exception as e:
        print(e)
        time.sleep(1)