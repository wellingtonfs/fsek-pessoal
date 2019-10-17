#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
import time

m1 = LargeMotor('outC') #Esquerdo
m2 = LargeMotor('outD') #Direito

gy = GyroSensor('in1')
gy.mode = 'GYRO-ANG'

def Modulo(x):
    if x < 0:
        return x * -1
    return x 

def Girar(ang):#errado
    atual = gy.value()
    while Modulo((gy.value() - atual)) < ang:
        m1.run_forever(speed_sp=100)
        m2.run_forever(speed_sp=-100)
    
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")

while True:
    Girar(90)
    time.sleep(2)

