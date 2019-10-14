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
#ir = UltrasonicSensor('in4')
# ir2 = InfraredSensor('in1')
# tou = TouchSensor('in4')
gy = GyroSensor('in1')

#Sensor_Cor[0].mode = 'COL-COLOR'
#Sensor_Cor[1].mode = 'COL-COLOR'
#us.mode = 'US-DIST-CM'
#us2.mode = 'US-DIST-CM'
#ir.mode = 'US-DIST-CM'
#ir.mode = 'IR-PROX'
# ir2.mode = 'IR-PROX'
gy.mode = 'GYRO-ANG'

ang = 90

def giraRobo(graus, tempo = 2): #90 > 0: direita else: esquerda
    razaoRobo = 5.25 / 3.0

    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(0.3)

    if graus > 0:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=40,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=40,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=-(razaoRobo*(graus*-1)),speed_sp=40,stop_action="brake")
        m2.run_to_rel_pos(position_sp=(razaoRobo*(graus*-1)),speed_sp=40,stop_action="brake")
    if tempo != 0:
        time.sleep(tempo)

while True:

    baseAngle = gy.value()
    print("Inicio loop")
    print("Angulo Base: ", baseAngle)

    giraRobo(90)

    time.sleep(0.5)

    angle = abs(gy.value() - baseAngle)
    diffAng = angle - 90

    print("Angulo Calculado: ", angle)
    print("Diferenca: ", diffAng)

    if(diffAng < 0):
        giraRobo(90)
    else:
        giraRobo(90)

    time.sleep(2)
