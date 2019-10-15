#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *

from ev3dev2.motor import OUTPUT_C, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import GyroSensor

import time, socket
import math

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
m3 = MediumMotor('outB')
m4 = MediumMotor('outA')

#Sensor_Cor = [ColorSensor('in1'), ColorSensor('in2')]
#Sensor_Cor[0] = ColorSensor('in1') #2
#Sensor_Cor[1] = ColorSensor('in2') #4
us = UltrasonicSensor('in3')
#us2 = UltrasonicSensor('in4')
#ir = InfraredSensor('in4')
#ir = UltrasonicSensor('in4')
# ir2 = InfraredSensor('in1')
# tou = TouchSensor('in4')

#Sensor_Cor[0].mode = 'COL-COLOR'
#Sensor_Cor[1].mode = 'COL-COLOR'
us.mode = 'US-DIST-CM'
#us2.mode = 'US-DIST-CM'
#ir.mode = 'US-DIST-CM'
#ir.mode = 'IR-PROX'
# ir2.mode = 'IR-PROX'

#mdiff = MoveDifferential(OUTPUT_D, OUTPUT_C, EV3EducationSetTire, 105)
#gy = GyroSensor(INPUT_1)
#gy.mode = 'GYRO-ANG'

def Mov_Garra_Sensor(Sentido, Pos): #0 = descer; 1 = subir;
    if Sentido: 
        if (us.value() < 400):
            while (us.value() < 100):
                m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    else: 
        while (us.value() > 100):
                m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    time.sleep(2)

def Mov_Garra_Analog(Sentido, Pos):
    if Sentido:
        m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
    else:
        m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")

Mov_Garra_Sensor(1, 100)
time.sleep(5)
Mov_Garra_Analog(0, 200)



'''
while True:
    print ("%d" %us.value())
'''