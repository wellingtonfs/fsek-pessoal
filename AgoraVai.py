#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import time, socket
import math

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
m3 = MediumMotor('outB')
m4 = MediumMotor('outA')

#Sensor_Cor = [ColorSensor('in1'), ColorSensor('in2')]
#Sensor_Cor[0] = ColorSensor('in1') #2
#Sensor_Cor[1] = ColorSensor('in2') #4
#us = UltrasonicSensor('in3')
#us2 = UltrasonicSensor('in4')
#ir = InfraredSensor('in4')
ir = UltrasonicSensor('in4')
# ir2 = InfraredSensor('in1')
# tou = TouchSensor('in4')

#Sensor_Cor[0].mode = 'COL-COLOR'
#Sensor_Cor[1].mode = 'COL-COLOR'
#us.mode = 'US-DIST-CM'
#us2.mode = 'US-DIST-CM'
ir.mode = 'US-DIST-CM'
#ir.mode = 'IR-PROX'
# ir2.mode = 'IR-PROX'

def Mov_Garra_Analog(Sentido, Pos):
    if Sentido:
        m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
    else:
        m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")

def Mov_Garra_Sensor(Sentido, Pos): #0 = descer; 1 = subir;
    if Sentido: 
        if (ir.value() < 400):
            while (ir.value() < 100):
                print (ir.value())
                m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    else: 
        while (ir.value() > 45):
                print (ir.value())
                m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    time.sleep(2)

Mov_Garra_Sensor(1, 100)
while True:
    print ("%d" %ir.value())
'''
while (ir.value() > 170):
    m1.run_forever(speed_sp=150)
    m2.run_forever(speed_sp=150)
    time.sleep(0.5)
m1.stop(stop_action="brake")
m2.stop(stop_action="brake")
time.sleep(0.5)

#Desce a garra
Mov_Garra_Analog(0, 100)

#Anda para tras     
while (ir.value() < 200):
    m1.run_forever(speed_sp=-150)
    m2.run_forever(speed_sp=-150)
    time.sleep(0.5)
m1.stop(stop_action="brake")
m2.stop(stop_action="brake")'''