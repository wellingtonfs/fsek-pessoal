#!/usr/bin/env python3
from ev3dev.ev3 import *
from ev3dev2.motor import OUTPUT_C, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import GyroSensor
import time

mdiff = MoveDifferential(OUTPUT_D, OUTPUT_C, EV3EducationSetTire, 105)
gy = GyroSensor(INPUT_1)
gy.mode = 'GYRO-ANG'

while True:
    baseAngle = gy.value()
    print("Inicio loop")
    print("Angulo Base: ", baseAngle)

    mdiff.turn_left(SpeedRPM(40), 90)

    time.sleep(0.5)

    angle = abs(gy.value() - baseAngle)
    diffAng = angle - 90

    print("Angulo Calculado: ", angle)
    print("Diferenca: ", diffAng)

    if(diffAng < 0):
        mdiff.turn_left(SpeedRPM(40), abs(diffAng))
    else:
        mdiff.turn_right(SpeedRPM(40), abs(diffAng))


    time.sleep(2)


# Anda Reto
# Gira


