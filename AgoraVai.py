#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import time, socket
import math

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
m3 = MediumMotor('outB')
m4 = MediumMotor('outA')

#Sensor_Cor = [ColorSensor('in1'), ColorSensor('in2')]
#Sensor_Cor[0] = ColorSensor('in1') #2
#Sensor_Cor[1] = ColorSensor('in2') #4
#us = UltrasonicSensor('in3')
#us2 = UltrasonicSensor('in4')
ir = InfraredSensor('in4')
# ir2 = InfraredSensor('in1')
# tou = TouchSensor('in4')

#Sensor_Cor[0].mode = 'COL-COLOR'
#Sensor_Cor[1].mode = 'COL-COLOR'
#us.mode = 'US-DIST-CM'
#us2.mode = 'US-DIST-CM'
ir.mode = 'IR-PROX'
# ir2.mode = 'IR-PROX'

#Anda até 27cm do gasoduto

while (ir.value() > 0 and ir.value() < 45):
    m3.run_to_rel_pos(position_sp=-50,speed_sp=150,stop_action="brake")
    m4.run_to_rel_pos(position_sp=50,speed_sp=150,stop_action="brake")
time.sleep(2)
      
while (ir.value() > 15): 
    m1.run_forever(speed_sp=150)
    m2.run_forever(speed_sp=150)
    time.sleep(0.5)
m1.stop(stop_action="brake")
m2.stop(stop_action="brake")
time.sleep(2)
'''
#Sobe a garra
m3.run_to_rel_pos(position_sp=-120,speed_sp=150,stop_action="brake")
m4.run_to_rel_pos(position_sp=120,speed_sp=150,stop_action="brake")

while (ir.value() > 10):
    m1.run_forever(speed_sp=150)
    m2.run_forever(speed_sp=150)
    time.sleep(0.5)
m1.stop(stop_action="brake")
m2.stop(stop_action="brake")
'''
#Desce a garra
m3.run_to_rel_pos(position_sp=120,speed_sp=150,stop_action="brake")
m4.run_to_rel_pos(position_sp=-120,speed_sp=150,stop_action="brake")

#Anda para tras     
while (ir.value() > 18):
    m1.run_forever(speed_sp=-150)
    m2.run_forever(speed_sp=-150)
    time.sleep(0.5)
m1.stop(stop_action="brake")
m2.stop(stop_action="brake")

#Desce a garra
m3.run_to_rel_pos(position_sp=-120,speed_sp=150,stop_action="brake")
m4.run_to_rel_pos(position_sp=120,speed_sp=150,stop_action="brake")

'''
while True:
    print ("%d" %ir.value())

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
    razaoRobo = 5.25 / 3.0

    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(0.3)

    if graus > 0:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=50,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=50,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=-(razaoRobo*(graus*-1)),speed_sp=50,stop_action="brake")
        m2.run_to_rel_pos(position_sp=(razaoRobo*(graus*-1)),speed_sp=50,stop_action="brake")
    if tempo != 0:
        time.sleep(tempo)

while True:

    m1.run_timed(time_sp=1000, speed_sp=150, stop_action="brake")
    m2.run_timed(time_sp=1000, speed_sp=150, stop_action="brake")
    time.sleep(2) 

    m1.reset()
    m2.reset()

    print("Antes: ", m1.position)
    print("Antes: ", m2.position)
    print ("SP: ", m1.position_sp)
    time.sleep(5)

    giraRobo(90)

    print("Depois: ", m1.position)
    print("Depois: ", m2.position)
    print ("SP: ", m1.position_sp)
    time.sleep(5)


ti, tf = -1, -1
m1.run_forever(speed_sp=150)
m2.run_forever(speed_sp=150)
if alinhar(2) == 0:
    m1.run_forever(speed_sp=150)
    m2.run_forever(speed_sp=150)
    time.sleep(2)
    giraRobo(-90)
while True:
    if (us.value() <= 570):
        while (110 < us.value() < 338):
            m1.run_forever(speed_sp=150)
            m2.run_forever(speed_sp=150)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        time.sleep(2)
        ti = time.time()

        while (338 < us.value() < 570):
            m1.run_forever(speed_sp=150)
            m2.run_forever(speed_sp=150)
            time.sleep(0.5)
        tf = time.time()
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        time.sleep(2)

    x = ((((tf-ti)/2)*1000)+1000)

    m1.run_timed(time_sp=x, speed_sp=-150, stop_action="brake")
    m2.run_timed(time_sp=x, speed_sp=-150, stop_action="brake")
    time.sleep(5)

    giraRobo(90)

    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    
    while (ir.value() > 27):
        print ("%d" %ir.value())
        m1.run_forever(speed_sp=150)
        m2.run_forever(speed_sp=150)
        time.sleep(2)

    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(30)
'''