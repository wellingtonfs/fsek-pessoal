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

speed = 600
alo = 600

while True:
    m3.run_forever(speed_sp=150)
    m4.run_forever(speed_sp=-150)
    print(m3.speed, " - ", m4.speed)

'''
def Para_Motor_Large(speed):
    speed = speed
    alo = speed

    while True:
        speed = alo

        m1.run_forever(speed_sp=speed)
        m2.run_forever(speed_sp=speed)

        print(m1.speed, " - ", m2.speed)
        time.sleep(0.5)

        speed = speed * 0.95

        if (m1.speed < speed) or (m2.speed < speed):
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
        break

def Para_Motor_Medium(Sentido, speed):
    speed = speed
    alo = speed

    while True:
        speed = alo

        if Sentido:
            m3.run_forever(speed_sp=(-1)*speed)
            m4.run_forever(speed_sp=speed)

            print(m1.speed, " - ", m2.speed)
            time.sleep(0.5)

            speed = speed * 0.95

            if (m1.speed < speed) or (m2.speed < speed):
                m3.stop(stop_action="brake")
                m4.stop(stop_action="brake")
        else:
            m3.run_forever(speed_sp=speed)
            m4.run_forever(speed_sp=(-1)*speed)

            print(m1.speed, " - ", m2.speed)
            time.sleep(0.5)

            speed = speed * 0.95

            if (m1.speed < speed) or (m2.speed < speed):
                m3.stop(stop_action="brake")
                m4.stop(stop_action="brake")
        break

#Para_Motor_Large(600)
Para_Motor_Medium(0, 150)

'''