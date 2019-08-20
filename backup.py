#!/usr/bin/env python3
from ev3dev.ev3 import *
import time
import math

m1 = LargeMotor('outD')
m2 = LargeMotor('outB')
cor = ColorSensor('in3')
cor2 = ColorSensor('in2')
giro = GyroSensor('in4')

giro.mode='GYRO-ANG'

cor.mode = 'COL-COLOR'
cor2.mode = 'COL-COLOR'

cor_ant = [1, 0]
branco = 6
cores = []

for i in [1,2,3,4,5]:
    ncor = [i, 0]
    cores.append(ncor)

def giraRobo(graus, sentido):
    razaoRobo = (2 * math.pi * 5.5) / (2 * math.pi * 3)
    if sentido:
        m2.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=700,stop_action="brake")
        m1.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=700,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=700,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=700,stop_action="brake")
    time.sleep(1)

def ArrumarAngulo(temp_dif, quallado):
    tempinho_novo = temp_dif * 1000
    if quallado:
        m1.run_timed(time_sp=tempinho_novo, speed_sp=600)
    else:
        m2.run_timed(time_sp=tempinho_novo, speed_sp=600)
    time.sleep(temp_dif)
    m1.run_forever(speed_sp=600)
    m2.run_forever(speed_sp=600)

def AchouCor():
    m1.run_timed(time_sp=500, speed_sp=600)
    m2.run_timed(time_sp=500, speed_sp=600)
    time.sleep(0.5)
    if cor_ant[1] == 1:
        cor_ant[1] = 2
    else:
        if cor_ant[1] == 2:
            cor_ant[1] = 0
        if x[1] == 0:
            giraRobo(85, True)
        elif x[1] == 1:
            giraRobo(85, False)
        else:
            if cor_ant[1] == 3:
                giraRobo(85, False)
                cor_ant[1] = 0
        cor_ant[0] = iterador
        m1.run_forever(speed_sp=600)
        m2.run_forever(speed_sp=600)

def AchouPreto():
    if cor_ant[1] == 2:
        cores[cor_ant[0]][1] = 2
        cor_ant[1] = 3
    else:
        y = cores[cor_ant[0]]
        y[1] = (y[1] + 1) % 3
        cores[cor_ant[0]][1] = y[1]
        cor_ant[1] = 1
    giraRobo(200, False)
    m1.run_forever(speed_sp=600)
    m2.run_forever(speed_sp=600)

m1.run_forever(speed_sp=600)
m2.run_forever(speed_sp=600)

iterador, tempinho = 0, 0
umavez = [True, False, False]
while True:
    x = cores[iterador]
    if cor.value() == x[0] and umavez[0]:
        if x[0] == 1:
            AchouPreto()
        else:
            AchouCor()

        umavez[0] = False
        umavez[1] = True
        umavez[2] = True

    if cor2.value() == branco and umavez[1]:
        if tempinho == 0:
            tempinho = time.time()
        else:
            ArrumarAngulo((time.time() - tempinho), True)
            time.sleep(0.2)
            umavez[0] = True
            tempinho = 0
        umavez[1] = False

    if cor.value() == branco and umavez[2]:
        if tempinho == 0:
            tempinho = time.time()
        else:
            ArrumarAngulo((time.time() - tempinho), False)
            time.sleep(0.2)
            umavez[0] = True
            tempinho = 0
        umavez[2] = False

    iterador = (iterador + 1) % 5


def blakeLine(): #Walk the black line to learning colors.
    global Estado
    vel_1, vel_2 = 200, 100
    x, y, z = -1, -1, -1
    giraRobo(90, False)
    while True:
        '''
        if 46 <= ir.value() <= 60:
            if Estado == 1:
                Estado = -1
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                giraRobo(90, True)
                Cor_Anterior = cor.value()
                dif_temp = 0
                Estado = 1
        '''
        print(cor.value())
        if cor.value() != 6:
            m1.run_timed(time_sp=1, speed_sp=vel_1)
            m2.run_timed(time_sp=1, speed_sp=vel_2)
            time.sleep(1)
        else:
            m1.run_to_rel_pos(position_sp=360, speed_sp=vel_2)
            m2.run_to_rel_pos(position_sp=360, speed_sp=vel_1)

    '''while True:
        if cor.value() != 6 and cor.value() != 6:
            m1.run_to_rel_pos(position_sp=360, speed_sp=500)
            m2.run_to_rel_pos(position_sp=360, speed_sp=570)
        else:
            m1.run_to_rel_pos(position_sp=360, speed_sp=570)
            m2.run_to_rel_pos(position_sp=360, speed_sp=500)
        if cor2.value() != 6 and cor2.value() != 1:
            if x == -1:
                x = cor2.value()
                print("color x: %d" %x)
            elif cor2.value() != x and y == -1:
                y = cor2.value()
                print("color y: %d" %y)
            elif cor2.value() != y and y != -1 and z == -1:
                z = cor2.value()
                print("color z: %d" %z)'''

    return [x,y,z]
