#!/usr/bin/env python3
from ev3dev.ev3 import *
import time, math

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
m3 = MediumMotor('outB')
cor = ColorSensor('in2')
cor2 = ColorSensor('in4')
ir = InfraredSensor('in1')
ir2 = InfraredSensor('in3')

cor.mode = 'COL-COLOR'
cor2.mode = 'COL-COLOR'
ir.mode = 'IR-PROX'
ir2.mode = 'IR-PROX'

def giraRobo(graus, sentido): #Essa função gira o robo para algum lado
    razaoRobo = (2 * math.pi * 5.5) / (2 * math.pi * 2.71)
    if sentido:
        m2.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
        m1.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=180,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=180,stop_action="brake")
    time.sleep(2)

def alinhar(c): #Essa função alinha o lego a uma cor especifica c.
    if cor.value() == c and cor2.value() == c:
        return 0
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

cor_anterior = -1
Estado = 0

while True: #enquanto nao chegar, ajustar para parar quando chegar
    if Estado == 0:
        while True:
            if ir.value() > 20:
                m1.run_to_rel_pos(position_sp=50, speed_sp=200)
                m2.run_to_rel_pos(position_sp=50, speed_sp=200)
            else:
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                m3.run_to_rel_pos(position_sp=50, speed_sp=200)
                time.sleep(1)
                while ir.value() != 0:
                    m1.run_to_rel_pos(position_sp=250, speed_sp=200)
                    m2.run_to_rel_pos(position_sp=250, speed_sp=200)
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                m3.run_to_rel_pos(position_sp=-300, speed_sp=200)
                time.sleep(1)
                break
        giraRobo(67, True)
        Estado = 1
    elif Estado == 1:
        if cor.value() == cor2.value():
            cor_anterior = cor.value()
        while True:
            m1.run_forever(speed_sp=250)
            m2.run_forever(speed_sp=250)
            time.sleep(0.03) #aqui

            if cor.value() != cor_anterior:
                print("esq: %d" %cor.value())
                print("dir: %d" %cor2.value())
                alinhar(cor.value())
                cor_anterior = cor.value()
                m1.run_forever(speed_sp=250)
                m2.run_forever(speed_sp=250)
                time.sleep(0.5) #aqui
                Estado = 2
                break
            elif cor2.value() != cor_anterior:
                print("esq: %d" %cor.value())
                print("dir: %d" %cor2.value())
                alinhar(cor2.value())
                cor_anterior = cor2.value()
                m1.run_forever(speed_sp=250)
                m2.run_forever(speed_sp=250)
                time.sleep(0.5) #aqui
                Estado = 2
                break
    elif Estado == 2:
        aux = True
        while True:
            if 46 <= ir2.value() <= 60 and aux:
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                giraRobo(143, False)
                m1.run_forever(speed_sp=-250)
                m2.run_forever(speed_sp=-250)
                time.sleep(7)
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                giraRobo(143, False)
                m3.run_to_rel_pos(position_sp=200, speed_sp=200)
                time.sleep(2)
                m1.run_forever(speed_sp=-250)
                m2.run_forever(speed_sp=-250)
                time.sleep(1.5)
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                m3.run_to_rel_pos(position_sp=-50, speed_sp=200)
                time.sleep(10)
                aux = False
            '''if cor.value() == 2 or cor2.value() == 2:
                m1.run_forever(speed_sp=-250)
                m2.run_forever(speed_sp=-250)
                time.sleep(2)
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                giraRobo(135, True)
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                time.sleep(10)'''
#teoricamente ele vai tentar ficar alinhado com cada cor, pode ter algum erro, da uma olhada

