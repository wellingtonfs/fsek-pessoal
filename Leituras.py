#!/usr/bin/env python3
from ev3dev.ev3 import *
import time

m1 = LargeMotor('outC')
m2 = LargeMotor('outD')

arq = open("Dados.txt", "w")
arq.write(" Leituras: \n\n")
arq.close()

def salvar(x):
    arq = open("Dados.txt", "a")
    s = "%d, %d\n" %(x[0], x[1])
    arq.write(s)
    arq.close()

m1.run_forever(speed_sp=200)
m2.run_forever(speed_sp=200)

while(True):
    salvar([m1.speed, m2.speed])