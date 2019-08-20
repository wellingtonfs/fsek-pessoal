#!/usr/bin/env python3
from ev3dev.ev3 import *
import time, math
from threading import *

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
cor = ColorSensor('in2')
cor2 = ColorSensor('in4')

cor.mode = 'COL-COLOR'
cor2.mode = 'COL-COLOR'

#deixar mais ou menos apontado pra direção do gasoduto

class Info(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            ss = "S1: %d\nS2: %d" %(cor.value(),cor2.value())
            print(ss)
            time.sleep(0.5)

lt = Info()
lt.start()

def alinhar(c): #Essa função alinha o lego a uma cor especifica c.
    m1.run_forever(speed_sp=-50)
    m2.run_forever(speed_sp=-50)
    time.sleep(2)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    m1.run_forever(speed_sp=50)
    m2.run_forever(speed_sp=50)
    while True:
        if cor.value() == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while cor.value() == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            #m1.run_forever(speed_sp=-150)
            m2.run_forever(speed_sp=100)
            while cor2.value() != c:
                if cor2.value() == 0:
                    return 1
                if cor.value() != c:
                    m1.run_forever(speed_sp=70)
                else:
                    m1.stop(stop_action="brake")
            return 0

        if cor2.value() == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while cor2.value() == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            m1.run_forever(speed_sp=100)
            #m2.run_forever(speed_sp=-150)
            while cor.value() != c:
                if cor.value() == 0:
                    return 1
                if cor2.value() != c:
                    m2.run_forever(speed_sp=70)
                else:
                    m2.stop(stop_action="brake")
            return 0

'''cor_anterior = 5
cor_anterior = cor.value()'''

while True: #enquanto nao chegar, ajustar para parar quando chegar
    m1.run_forever(speed_sp=300)
    m2.run_forever(speed_sp=300)

    if cor.value() == 1 or cor2.value() == 1:
        alinhar(1)
        m1.run_forever(speed_sp=300)
        m2.run_forever(speed_sp=300)
        time.sleep(1)
'''
    if cor.value() != cor_anterior:
        alinhar(cor.value())
        cor_anterior = cor.value()
    elif cor2.value() != cor_anterior:
        alinhar(cor2.value())
        cor_anterior = cor2.value()

'''

#teoricamente ele vai tentar ficar alinhado com cada cor, pode ter algum erro, da uma olhada
