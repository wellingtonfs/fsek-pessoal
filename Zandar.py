#!/usr/bin/env python3
from ev3dev.ev3 import *
import time

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')

def giraRobo(graus, tempo = 2): #90 > 0: direita else: esquerda
    razaoRobo = 5.25 / 3.0
    if graus > 0:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=180,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=-(razaoRobo*(graus*-1)),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=(razaoRobo*(graus*-1)),speed_sp=180,stop_action="brake")
    if tempo != 0:
        time.sleep(tempo)

while True:
    giraRobo(90)
    giraRobo(-90)
    giraRobo(180)
    giraRobo(-180, 5)