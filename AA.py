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

#Sensor_Cor[0].mode = 'COL-COLOR'
#Sensor_Cor[1].mode = 'COL-COLOR'
#us.mode = 'US-DIST-CM'
#us2.mode = 'US-DIST-CM'
#ir.mode = 'US-DIST-CM'
#ir.mode = 'IR-PROX'
# ir2.mode = 'IR-PROX'

m1.run_to_rel_pos(position_sp=5000,speed_sp=150,stop_action="brake")
m2.run_to_rel_pos(position_sp=5000,speed_sp=150,stop_action="brake")