#!/usr/bin/env python3
from ev3dev.ev3 import *
import time, math

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')

m1.run_forever(speed_sp=300)
m2.run_forever(speed_sp=300)

while True:
    pass
