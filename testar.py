#!/usr/bin/env python3
from ev3dev.ev3 import *
import time
import math

#m1 = LargeMotor('outD')
#m2 = LargeMotor('outB')
#ts = TouchSensor('in4')

giro = GyroSensor('in4') #caso nao de, tire o 'in2', deixa só ()

giro.mode='GYRO-ANG'

units = giro.units

while True:
    print(str(giro.value()) + " " + units)
    time.sleep(1)

'''while not ts.value():
    angle = giro.value()
    print(str(angle) + " " + units)
    Sound.tone(1000+angle*10, 1000).wait()
    sleep(0.5)
'''
