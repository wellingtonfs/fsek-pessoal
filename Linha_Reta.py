#!/usr/bin/env python3
import termios, tty, sys
from ev3dev.ev3 import *
from threading import *
import time

m1 = LargeMotor('outA')
m2 = LargeMotor('outD')

gy = GyroSensor('in1')
gy.mode = 'GYRO-ANG'

class andar(Thread):
    def __init__(self):
        self.andando = False
        self.parando = False
        self.vel = 200
        self.ang = 0.2
        Thread.__init__(self)

    def run(self):
        global gy
        while True:
            if self.andando:
                angulo_base = gy.value()
                if self.ang != 0.2:
                    angulo_base = self.ang
                speed1, speed2 = self.vel, self.vel
                while self.parando == False:
                    g = gy.value()
                    if g < angulo_base:
                        speed1 = self.vel - 20
                    elif g > angulo_base:
                        speed2 = self.vel - 20
                    else:
                        speed1, speed2 = self.vel, self.vel
                    m1.run_forever(speed_sp=speed1)
                    m2.run_forever(speed_sp=speed2)
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")

                self.andando = False
                self.parando = False
                self.ang = 0.2

    def andar(self, speed = 200, angulo = 0.2):
        self.andando = True
        self.vel = speed
        self.ang = angulo

    def parar(self):
        self.parando = True

lego = andar()
lego.daemon = True
lego.start()

while True:
    a = eval(input("Digite um numero: "))
    if a == 1:
        lego.andar()
    elif a > 1:
        lego.andar(angulo = a)
    else:
        lego.parar()
    