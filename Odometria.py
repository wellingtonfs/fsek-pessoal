#!/usr/bin/env python3
from ev3dev.ev3 import *
import time
import math

#Motors
m1 = LargeMotor('OutD') #Left_Motor
m2 = LargeMotor('OutC') #Right_Motor
m3 = MediumMotor('OutB') #Claw_Motor

#ColorSensors
cor = ColorSensor('in2') #Left_ColorSensor
cor.mode = 'COL-COLOR'
cor2 = ColorSensor('in4') #Right_ColorSensor
cor2.mode = 'COL-COLOR'
#Sensors 
#ir = InfraredSensor('in1') #Infrared_Sensor
#ir.mode = 'IR-PROX'
#us = UltrasonicSensor('in3') #Ultrasonic_Sensor
#us.mode = 'US-DIST-CM'

'''def rotateRobot(degrees, way): #Odometry
    razaoRobo = (2 * math.pi * 5.5) / (2 * math.pi * 3)
    print(razaoRobo)
    print(razaoRobo*degrees)
    print("-")
    if way:
        m1.run_to_rel_pos(position_sp=int(razaoRobo*degrees), speed_sp=200, stop_action="brake")
        m2.run_to_rel_pos(position_sp=int(-(razaoRobo*degrees)), speed_sp=200, stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=int(-(razaoRobo*degrees)), speed_sp=200, stop_action="brake")
        m2.run_to_rel_pos(position_sp=int(razaoRobo*degrees), speed_sp=200, stop_action="brake")
    time.sleep(2)'''

def giraRobo(graus, sentido): #True = Esquerda, False = Direita
    razaoRobo = (2 * math.pi * 5.5) / (2 * math.pi * 2.55)
    print(razaoRobo)
    if sentido:
        m1.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=180,stop_action="brake")
    time.sleep(2)

while True:
    giraRobo(90, True)
    giraRobo(180, True)

    #rotateRobot(90,True)
    #rotateRobot(180,True)