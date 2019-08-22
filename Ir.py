#!/usr/bin/env python3
from ev3dev.ev3 import *
from threading import *
import time
import math

a = 2.47

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')

def giraRobo(graus, sentido): #True = Esquerda, False = Direita
    global a
    razaoRobo = (2 * math.pi * 5.5) / (2 * math.pi * a)
    if sentido:
        m1.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=180,stop_action="brake")
    time.sleep(2)
    a += 0.01

while True:
    print(str(a))
    giraRobo(90, True)
    time.sleep(5)