#!/usr/bin/env python3
from ev3dev.ev3 import *
from threading import *
import time
import math

#------VARIÁVEIS DO PROGRAMA

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
m3 = MediumMotor('outB')
cor = ColorSensor('in2')
cor2 = ColorSensor('in4')
ir = InfraredSensor('in3')
ir2 = InfraredSensor('in1')

cor.mode = 'COL-COLOR'
cor2.mode = 'COL-COLOR'
ir.mode = 'IR-PROX'
ir2.mode = 'IR-PROX'

while True:
    ir.value()
    print("ir: %d" %ir.value())
    time.sleep(0.7)