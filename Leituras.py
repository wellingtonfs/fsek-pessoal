#!/usr/bin/env python3
from ev3dev.ev3 import *
import time

us = UltrasonicSensor('in4')
us.mode = 'US-DIST-CM'

gy = GyroSensor('in1')
gy.mode = 'GYRO-ANG'
  
ir = InfraredSensor('in2')
ir.mode = 'IR-PROX'

while(True):
    print("%d  -  %d  -  %d" %(us.value(), ir.value(), gy.value()))
    time.sleep(0.5)