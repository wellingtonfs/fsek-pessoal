#!/usr/bin/env python3
#coding: utf-8
import socket, json
from ev3dev.ev3 import *
from threading import *

import time
import math

gy = GyroSensor('in3')
gy.mode = 'GYRO-ANG'

ub = UltrasonicSensor('in4')
ub.mode = 'US-DIST-CM'

time.sleep(1)
print("iniciando..")

g = gy.value()

while True:
    try:
        while True:
            l = ub.value()
            if l > 2500:
                continue

            s = "Leitura: %d" %l

            v = abs(gy.value() - g)
            if v != 0:
                s += ", ang: %d" %v
                l *= math.cos(v/57.2958)

            s += ", correcao: %d" %l

            print(s)

            time.sleep(1)

    except:
        a = input("Continuar? ")
        if a == 'n':
            exit()
            quit()