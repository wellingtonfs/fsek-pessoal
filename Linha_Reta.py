#!/usr/bin/env python3
import termios, tty, sys
from ev3dev.ev3 import *
from threading import *
import time

m1 = LargeMotor('outC')
m2 = LargeMotor('outD')

gy = GyroSensor('in1')
gy.mode = 'GYRO-ANG'

class andar(Thread):
    def __init__(self):
        self.andando = False
        self.parando = False
        self.vel = 200
        self.ang = 0.2
        self.parado = False
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
                    if g > angulo_base:
                        speed1 = self.vel - 20
                    elif g < angulo_base:
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
                self.parado = False

    def andar(self, speed = 200, angulo = 0.2):
        while self.parado:
            pass
        self.andando = True
        self.parando = False
        self.vel = speed
        self.ang = angulo

    def parar(self):
        self.parando = True
        self.parado = True

lego = andar()
lego.daemon = True
lego.start()

def Ir_Pos_Matriz(pIni, pFim, angulo): #testar em outro arquivo..
    tempo_andar = time.time()
    while True:
        if pIni == pFim:
            return 0
        elif pIni < pFim:
            if pIni < pFim and (time.time() - tempo_andar) > 0.85:
                lego.andar(speed = 150, angulo = angulo)
                pIni += 1
                tempo_andar = time.time()
            else:
                if pIni == pFim:
                    return 0
        else:
            if pIni > pFim and (time.time() - tempo_andar) > 0.85:
                lego.andar(speed = -150, angulo = angulo)
                pIni -= 1
                tempo_andar = time.time()
            else:
                if pIni == pFim:
                    return 0

def Girar(ang):
    atual = gy.value()
    if ang > 0:
        ang -= 3
        while abs(gy.value() - atual) < abs(ang):
            m1.run_forever(speed_sp=100)
            m2.run_forever(speed_sp=-100)
    else:
        ang += 3
        while abs(gy.value() - atual) < abs(ang):
            m1.run_forever(speed_sp=-100)
            m2.run_forever(speed_sp=100)
    
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")

while True:
    a = input("Digite um numero: ")
    if a[0] == '-':
        lego.andar(speed=-200)
    elif a[0] == '+':
        lego.andar(speed=200)
    elif a[0] == '0':
        lego.parar()
    elif a[0] == '.':
        Ir_Pos_Matriz(int(a[1]), int(a[2]), gy.value())
    elif a[0] == '<':
        Girar(-90)
    elif a[0] == '>':
        Girar(90)
        
    