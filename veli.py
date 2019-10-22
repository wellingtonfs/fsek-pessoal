#!/usr/bin/env python3
from ev3dev.ev3 import *
import time

m1 = LargeMotor('outC')
m2 = LargeMotor('outD')

arq = open("Dados.txt", "w")
arq.write(" Leituras: \n\n")
arq.close()

def Para_Motor_Large(speed):
    while True:
        m1.run_forever(speed_sp=speed)
        m2.run_forever(speed_sp=speed)

        if (m1.speed >= speed) and (m2.speed >= speed):
            while True:
                m1.run_forever(speed_sp=speed)
                m2.run_forever(speed_sp=speed)

                limite = speed * 0.95

                if (m1.speed <= limite) or (m1.speed <= limite):
                    m1.stop(stop_action="brake")
                    m2.stop(stop_action="brake")
                    break
            break


def salvar(x):
    arq = open("Dados.txt", "a")
    s = "%d, %d\n" %(x[0], x[1])
    arq.write(s)
    arq.close()

m1.run_forever(speed_sp=1000)
m2.run_forever(speed_sp=1000)

while(True):
    salvar([m1.speed, m2.speed])