#!/usr/bin/env python3
from ev3dev.ev3 import *
import time

m1 = LargeMotor('outA')
m2 = LargeMotor('outB')

t = TouchSensor('in2')
t.mode = 'TOUCH'

giro = GyroSensor('in1')
giro.mode='GYRO-ANG'

def Modulo(x):
    if x < 0:
        return x * -1
    return x

def giraRobo(graus):
    Valor_angulo = giro.value()
    if graus > 0:
        while Modulo(giro.value() - Valor_angulo) < (graus - 14):
            m1.run_to_rel_pos(position_sp=300, speed_sp=120)
            m2.run_to_rel_pos(position_sp=-300, speed_sp=120)
    else:
        while Modulo(giro.value() - Valor_angulo) < ((graus + 14) * -1):
            m1.run_to_rel_pos(position_sp=-300, speed_sp=200)
            m2.run_to_rel_pos(position_sp=300, speed_sp=200)
    Valor_angulo = giro.value()
    print(Valor_angulo)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")

print("Iniciou")

while True:
    temp = time.time()
    while t.value():
        pass
    if (time.time() - temp) > 2.5:
        giraRobo(360)
        #print("%.2f" %(time.time() - temp))
    elif (time.time() - temp) > 1:
        giraRobo(-180)
        #print("%.2f" %(time.time() - temp))
    elif (time.time() - temp) > 0.2:
        giraRobo(90)
        #print("%.2f" %(time.time() - temp))



    