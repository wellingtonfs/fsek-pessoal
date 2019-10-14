#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
import time

ir = InfraredSensor('in4')
ir.mode = 'IR-PROX'

while True:
    print("IR: %d" %ir.value())
    time.sleep(0.5)
