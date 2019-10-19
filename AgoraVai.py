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

def Para_Motor_Large(speed):
    speed = speed
    alo = speed
    sumSpeed = 0

    while True:
        speed = alo

        m1.run_forever(speed_sp=speed)
        m2.run_forever(speed_sp=speed)

        for i in range(0, 10):
            sumSpeed = sumSpeed + m3.speed
        speed = speed * 0.95
        sumSpeed = sumSpeed / 10

        if (sumSpeed < speed):
            m3.stop(stop_action="brake")
            m4.stop(stop_action="brake")
        break

def Para_Motor_Medium(speed):
    speed = speed
    alo = speed
    sumSpeed = 0

    while True:
        speed = alo

        m3.run_forever(speed_sp=speed)
        m4.run_forever(speed_sp=(-1)*speed)

        for i in range(0, 10):
            sumSpeed = sumSpeed + m3.speed
        speed = speed * 0.95
        sumSpeed = sumSpeed / 10

        if (sumSpeed < speed):
            m3.stop(stop_action="brake")
            m4.stop(stop_action="brake")
    break

#Para_Motor_Large(600)
Para_Motor_Medium(0, 600)