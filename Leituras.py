#!/usr/bin/env python3
from ev3dev.ev3 import *
import time

ir = UltrasonicSensor('in4')
ir.mode = 'US-DIST-CM'

gy = GyroSensor('in1')
gy.mode = 'GYRO-ANG'

us = UltrasonicSensor('in2')
us.mode = 'US-DIST-CM'
  
while(True):
    print("%d  -  %d  -  %d" %(us, ir, gy))
    time.sleep(0.5)