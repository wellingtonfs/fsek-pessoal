#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *

from ev3dev2.motor import OUTPUT_C, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import GyroSensor

import time, socket
import math

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
m3 = MediumMotor('outB')
m4 = MediumMotor('outA')

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

def Para_Motor_Medium(speed):
    while True:
        m3.run_forever(speed_sp=speed)
        m4.run_forever(speed_sp=-speed)

        sumSpeedM3 = 0
        sumSpeedM4 = 0

        for i in range(0, 15):
            if (i < 5):
                continue
            sumSpeedM3 = sumSpeedM3 + m3.speed
            sumSpeedM4 = sumSpeedM4 + m4.speed
        limite = speed * 0.95
        
        sumSpeedM3 = sumSpeedM3 / 10
        sumSpeedM4 = abs(sumSpeedM4 / 10)

        if (sumSpeedM3 < limite) or (sumSpeedM4 < limite):
            m3.stop(stop_action="brake")
            m4.stop(stop_action="brake")
            break

def Mov_Garra_Analog(Sentido, Pos):
    if Sentido:
        m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
        time.sleep(1)
    else:
        m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
        time.sleep(1)

def Mov_Garra_Sensor(Sentido, Pos): #0 = descer; 1 = subir;
    if Sentido: 
        if (us.value() < 400):
            while (us.value() < 100):
                m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    else: 
        while (us.value() > 45):
                m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    time.sleep(2)

def Cano_Suporte(pos):
    Mov_Garra_Analog(1, 100)
    Para_Motor_Large(600)
    time.sleep(2)
    Mov_Garra_Analog(0, 180)

    m1.run_to_rel_pos(position_sp=-pos,speed_sp=250,stop_action="brake")
    m2.run_to_rel_pos(position_sp=-pos,speed_sp=250,stop_action="brake")

Cano_Suporte(200)