#!/usr/bin/env python3
from ev3dev.ev3 import *
from threading import *
import time
import math

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
m3 = MediumMotor('OutB')
cor = ColorSensor('in2')
cor2 = ColorSensor('in4')
ir = InfraredSensor('in1')
#us2 = UltrasonicSensor('in3')

cor.mode = 'COL-COLOR'
cor2.mode = 'COL-COLOR'
ir.mode = 'IR-PROX'
#us2.mode = 'US-DIST-CM'

def converter():
    xyz[0] = first_Color
    xyz[1] = second_Color
    xyz[2] = third_Color

x, y, z = -1, -1, -1

'''
Tabela de cores
0 = Sem Cor
1 = Preto
2 = Azul
3 = Verde
4 = Amarelo
5 = Vermelho
6 = Branco
7 = Marrom
'''

while True:
    if cor.value() != 6 and cor2.value() != 6:
        m1.run_to_rel_pos(position_sp=360, speed_sp=500)
        m2.run_to_rel_pos(position_sp=360, speed_sp=570)
    else:
        m1.run_to_rel_pos(position_sp=360, speed_sp=570)
        m2.run_to_rel_pos(position_sp=360, speed_sp=500)
    if cor2.value() != 6 and cor2.value() != 1 and cor2.value() != 3:
        if x == -1:
            x = cor2.value()
            print("cor x: %d" %x)
        elif cor2.value() != x and y == -1:
            y = cor2.value()
            print("cor y: %d" %y)
        elif cor2.value() != y and y != -1 and z == -1:
            z = cor2.value()
            print("cor z: %d" %z)
    return [xyz]
    if ir.value() <= 20:
        converter()
        print("%i, %i, %i", %first_Color, %second_Color, %third_Color)
        m3.run_to_rel_pos(position_sp=50, speed_sp=200)
        time.sleep(0.03)
        m1.run_to_rel_pos(position_sp=360, speed_sp=50, stop_action="brake")
        m2.run_to_rel_pos(position_sp=360, speed_sp=50, stop_action="brake")
    return 0
