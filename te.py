#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *

from threading import *
from ev3dev2.motor import OUTPUT_C, OUTPUT_D, MoveTank
import time, socket, json
import math

tank = MoveTank(OUTPUT_C, OUTPUT_D)
m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
m3 = MediumMotor('outB')
m4 = MediumMotor('outA')
us = UltrasonicSensor('in3')
us2 = UltrasonicSensor('in4')
us3 = UltrasonicSensor('in2')
gy = GyroSensor('in1')
#Sensor_Cor = [ColorSensor('in2'), ColorSensor('in1')] #2 = Esquerdo, 1 = Direito

us.mode = 'US-DIST-CM'
us2.mode = 'US-DIST-CM'
us3.mode = 'US-DIST-CM'
gy.mode = 'GYRO-ANG'
#Sensor_Cor[0].mode = 'COL-COLOR'
#Sensor_Cor[1].mode = 'COL-COLOR'


def alinhar_ultra(): #Essa função alinha o lego a uma cor especifica c.
    if us.value() > 100 and us2.value() > 100:
        return 0
    if us.value() > 100:
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        while us.value() > 100:
            m1.run_forever(speed_sp=-50)
            m2.run_forever(speed_sp=-50)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        #m1.run_forever(speed_sp=-150)
        m2.run_forever(speed_sp=100)
        while us2.value() < 100:
            pass

    if us2.value() > 100:
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        while us2.value() > 100:
            m1.run_forever(speed_sp=-50)
            m2.run_forever(speed_sp=-50)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        m1.run_forever(speed_sp=100)
        #m2.run_forever(speed_sp=-150)
        while us.value() < 100:
            pass

    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(1)
    return 0

while True:
    m1.run_forever(speed_sp=150)
    m2.run_forever(speed_sp=150)
    if (us.value() > 100) or (us2.value() > 100):
        alinhar_ultra()
        break