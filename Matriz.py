#!/usr/bin/env python3
from ev3dev.ev3 import *
from threading import *
import time
import math

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')

ir = InfraredSensor('in2')
ir.mode = 'IR-PROX'

class par(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            print("IR: %d" %ir.value())
            time.sleep(0.5)

p = par()
p.daemon = True
p.start()

m1.run_forever(speed_sp=100)
m2.run_forever(speed_sp=100)
while True:
    a = input("De enter para sair..")
    break