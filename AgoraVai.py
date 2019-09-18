#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import time, socket
import math

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
# m3 = MediumMotor('outB')

# cor = ColorSensor('in1') #2
# cor2 = ColorSensor('in2') #4
# us = UltrasonicSensor('in3')
# us2 = UltrasonicSensor('in4')
# ir = InfraredSensor('in3')
# ir2 = InfraredSensor('in1')
tou = TouchSensor('in4')

# cor.mode = 'COL-COLOR'
# cor2.mode = 'COL-COLOR'
# us.mode = 'US-DIST-CM'
# us2.mode = 'US-DIST-CM'
# ir.mode = 'IR-PROX'
# ir2.mode = 'IR-PROX'

# while True:
#     tempo_inicio, tempos_pista, anterior_leitura = -1, [], 0
#     tempo_dez, tempo_quinze, tempo_vinte = 0,0,0
#     if alinhar(3) == 0: #O zero significa que já está alinhado
#     m1.run_forever(speed_sp=150)
#     m2.run_forever(speed_sp=150)
#     time.sleep(2)
#     m1.stop(stop_action="brake")
#     m2.stop(stop_action="brake")
#     giraRobo(-90, 3)
#     while True:
#         m1.run_forever(speed_sp=150)
#         m2.run_forever(speed_sp=150)
#         if us.value() > 36 or us2.value() > 36: #Evita de cair da p
#             m1.stop_action("brake")
#             m2.stop_action("brake")
#             giraRobo(180)
#             if len(tempos_pista) > 1: 
#                 tempos_pista.append(time.time())
#         elif anterior_leitura == -1:
#             tempos_pista.append(time.time()) 
#             anterior_leitura = Comm.ir2_value
#         elif (Comm.ir2_value - anterior_leitura) > 20: #Descobre um vao
#             tempos_pista.append(time.time())
#             anterior_leitura = Comm.ir2_value
#             if tempo_inicio == 0:
#                 tempo_inicio = time.time()
#         elif (Comm.ir2_value - anterior_leitura) < 20: #Vao fechou
#             tempos_pista.append(time.time())
#             anterior_leitura = Comm.ir2_value
#             if (time.time() - tempo_inicio) > 0:
#                 print(str(time.time() - tempo_inicio))
#                 time.sleep(15)
well = False

while True:
    if tou.value() == True:
        well = True
        if well:
            well = False
        else:
            well = True
        time.sleep(0.3)
    if well:
        m1.run_forever(speed_sp=150)
        m2.run_forever(speed_sp=150)
        time.sleep(1)