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
#us = UltrasonicSensor('in2')
us = UltrasonicSensor('in3')
us2 = UltrasonicSensor('in4')
Sensor_Cor = [ColorSensor('in1'), ColorSensor('in2')] #1 = Esquerdo, 2 = Direito

us.mode = 'US-DIST-CM'
us2.mode = 'US-DIST-CM'
Sensor_Cor[0].mode = 'COL-COLOR'
Sensor_Cor[1].mode = 'COL-COLOR'

'''
def Encontrar_Pos():
    while True:
        if Sensor_Cor[0].value() == 1 or Sensor_Cor[1].value() == 1: #Se achar Preto
            Al = alinhar(1)
            if Al == 1:
                Emergencia(80)
            elif Al == 2:
                Emergencia(-80)
            else:
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                return 0
        elif Sensor_Cor[0].value() == 3 or Sensor_Cor[1].value() == 3: #Se achar Verde
            Emergencia(180)
        elif 50 < us.value() < 300:
            print ("Caindo")
            print (us.value())
            Emergencia(90)
        elif 50 < us2.value() < 300:
            print ("Caindo")
            print (us2.value())
            Emergencia(-90)

        m1.run_forever(speed_sp=300)
        m2.run_forever(speed_sp=300)
'''
def Emergencia(graus):
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(0.5)

    m1.run_to_rel_pos(position_sp=-400,speed_sp=150,stop_action="brake")
    m2.run_to_rel_pos(position_sp=-400,speed_sp=150,stop_action="brake")
    time.sleep(3)
    giraRobo(graus)
    m1.run_forever(speed_sp=300)
    m2.run_forever(speed_sp=300)
'''
def gyro(an):
    baseAngle = gy.value()

    mdiff.turn_left(SpeedRPM(40), an)
    time.sleep(0.5)

    angle = abs(gy.value() - baseAngle)
    diffAng = angle - an

    if(diffAng < 0):
        mdiff.turn_left(SpeedRPM(40), abs(diffAng))
    else:
        mdiff.turn_right(SpeedRPM(40), abs(diffAng))
    time.sleep(2)
'''
def giraRobo(graus, tempo = 2): #90 > 0: direita else: esquerda
    razaoRobo = 5.25 / 3.0

    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(0.3)

    if graus > 0:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=280,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=280,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=-(razaoRobo*(graus*-1)),speed_sp=280,stop_action="brake")
        m2.run_to_rel_pos(position_sp=(razaoRobo*(graus*-1)),speed_sp=280,stop_action="brake")
    if tempo != 0:
        time.sleep(tempo)

def alinhar(c, Sentido): #Essa função alinha o lego a uma cor especifica c.
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
    m1.run_forever(speed_sp=Sentido)
    m2.run_forever(speed_sp=Sentido)
    time.sleep(1)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    return 0

def alinhar_ultra(): #Essa função alinha o lego a uma cor especifica c.
    if us.value() > 140 and us2.value() > 140:
        return 0
    while True:
        if us.value() > 140:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while us.value() > 140:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            #m1.run_forever(speed_sp=-150)
            m2.run_forever(speed_sp=100)
            while us2.value() < 140:
                if us2.value() > 140:
                    return 1
                if us.value() < 140:
                    m2.stop(stop_action="brake")
                    m1.run_forever(speed_sp=70)
                else:
                    m1.stop(stop_action="brake")
                    m2.run_forever(speed_sp=100)
            break

        if us2.value() > 140:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while us2.value() > 140:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            m1.run_forever(speed_sp=100)
            #m2.run_forever(speed_sp=-150)
            while us.value() < 140:
                if us.value() > 140:
                    return 1
                if us2.value() < 140:
                    m1.stop(stop_action="brake")
                    m2.run_forever(speed_sp=70)
                else:
                    m1.run_forever(speed_sp=100)
                    m2.stop(stop_action="brake")
            break

    m1.run_forever(speed_sp=-250)
    m2.run_forever(speed_sp=-250)
    time.sleep(1)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    return 0

while True:
    m1.run_forever(speed_sp=250)
    m2.run_forever(speed_sp=250)
    if alinhar(1, -250) == 0:
        giraRobo(-90)
        m1.run_forever(speed_sp=250)
        m2.run_forever(speed_sp=250)
        if (us.value() > 140) or (us2.value() > 140):
            alinhar_ultra()