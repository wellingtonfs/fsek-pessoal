#!/usr/bin/env python3
from ev3dev.ev3 import *
import time

motor_left = LargeMotor('outC')
motor_right = LargeMotor('outD')

motor_a = MediumMotor('outA')
motor_b = MediumMotor('outB')

motor_left.run_forever(speed_sp=600)
motor_right.run_forever(speed_sp=600)

while True:
    print(motor_left.speed, " - ", motor_right.speed)
    time.sleep(0.5)
