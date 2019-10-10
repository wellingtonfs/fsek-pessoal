#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import socket, time
import math

ir = InfraredSensor('in2')
ir.mode = 'IR-PROX'

while True: 
    print(ir.value())
    time.sleep(.2)