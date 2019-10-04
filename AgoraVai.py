#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import time, socket
import math

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
# m3 = MediumMotor('outB')

Sensor_Cor = [ColorSensor('in1'), ColorSensor('in2')]
#Sensor_Cor[0] = ColorSensor('in1') #2
#Sensor_Cor[1] = ColorSensor('in2') #4
us = UltrasonicSensor('in3')
# us2 = UltrasonicSensor('in4')
# ir = InfraredSensor('in3')
# ir2 = InfraredSensor('in1')
# tou = TouchSensor('in4')

Sensor_Cor[0].mode = 'COL-COLOR'
Sensor_Cor[1].mode = 'COL-COLOR'
us.mode = 'US-DIST-CM'
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
'''well = False

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
        time.sleep(1)'''

'''while True:
    print ("%d" %us.value())'''

def alinhar(c): #Essa função alinha o lego a uma cor especifica c.
    if Sensor_Cor[0].value() == c and Sensor_Cor[1].value() == c:
        return 0
    while True:
        if Sensor_Cor[0].value() == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while Sensor_Cor[0].value() == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            #m1.run_forever(speed_sp=-150)
            m2.run_forever(speed_sp=100)
            while Sensor_Cor[1].value() != c:
                if Sensor_Cor[1].value() == 0:
                    return 1
                if Sensor_Cor[0].value() != c:
                    m2.stop(stop_action="brake")
                    m1.run_forever(speed_sp=70)
                else:
                    m1.stop(stop_action="brake")
                    m2.run_forever(speed_sp=100)
                if 40 < us2.value() < 400:
                    return 2
            break

        if Sensor_Cor[1].value() == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while Sensor_Cor[1].value() == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            m1.run_forever(speed_sp=100)
            #m2.run_forever(speed_sp=-150)
            while Sensor_Cor[0].value() != c:
                if Sensor_Cor[0].value() == 0:
                    return 1
                if Sensor_Cor[1].value() != c:
                    m1.stop(stop_action="brake")
                    m2.run_forever(speed_sp=70)
                else:
                    m1.run_forever(speed_sp=100)
                    m2.stop(stop_action="brake")
                if 40 < us.value() < 400:
                    return 1
            break

    m1.run_forever(speed_sp=250)
    m2.run_forever(speed_sp=250)
    time.sleep(0.5)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    return 0

def giraRobo(graus, tempo = 2): #90 > 0: direita else: esquerda
    razaoRobo = 5.5 / 3.0
    if graus > 0:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=180,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=-(razaoRobo*(graus*-1)),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=(zaoRobo*(graus*-1)),speed_sp=180,stop_action="brake")
    if tempo != 0:
        time.sleep(tempo)

m1.run_forever(speed_sp=150)
m2.run_forever(speed_sp=150)

if alinhar(3) == 0:
    m1.run_to_rel_pos(position_sp=700,speed_sp=150,stop_action="brake")
    m2.run_to_rel_pos(position_sp=700,speed_sp=150,stop_action="brake")
    time.sleep(2)
    giraRobo(-90)       
'''
while (us.value() > 230):
    m1.run_forever(speed_sp=150)
    m2.run_forever(speed_sp=150)
    time.sleep(0.3)

m1.stop(stop_action="brake")
m2.stop(stop_action="brake")

while (us.value() > 230):
    m1.run_forever(speed_sp=-150)
    m2.run_forever(speed_sp=-150)
'''