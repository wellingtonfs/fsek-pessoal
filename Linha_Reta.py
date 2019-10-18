#!/usr/bin/env python3
import termios, tty, sys
from ev3dev.ev3 import *
from threading import *
import time

m1 = LargeMotor('outA')
m2 = LargeMotor('outD')

gy = GyroSensor('in1')
gy.mode = 'GYRO-ANG'

ir = False

class paralelo(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global ir
        while True:
            if ir:
                print("%d" %gy.value())
                time.sleep(0.5)

pp = paralelo()
pp.daemon = True
pp.start()

def andar(tempo_and):
    t_i = time.time()
    angulo_base = gy.value()
    speed1, speed2 = 200, 200
    while (time.time() - t_i) <= tempo_and:
        g = gy.value()
        if g < angulo_base:
            speed1 = 180
        elif g > angulo_base:
            speed2 = 180
        else:
            speed1, speed2 = 200, 200
        m1.run_forever(speed_sp=speed1)
        m2.run_forever(speed_sp=speed2)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")

while True:
    a = eval(input("Digite um tempo: "))
    ir = True
    andar(a)
    ir = False