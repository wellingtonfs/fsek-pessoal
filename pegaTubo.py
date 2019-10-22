#!/usr/bin/env python3
from ev3dev.ev3 import *
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveTank, MediumMotor, LargeMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import GyroSensor
import time

tank = MoveTank(OUTPUT_C, OUTPUT_D)

Sensor_Cor[0].mode = 'COL-COLOR'
Sensor_Cor[1].mode = 'COL-COLOR'

def rotateTo(degrees, speed = 10, linearSpeed = 0):
    # Clockwise
    angleBase = gy.value()

    if degrees > 0:
        left_speed = speed + linearSpeed
        right_speed = -speed + linearSpeed
    else:
        left_speed = -speed + linearSpeed
        right_speed = speed + linearSpeed

    degrees = abs(degrees)

    tank.on(left_speed, right_speed)
    while abs(gy.value() - angleBase) <= degrees:
        pass
    tank.stop()

def walkUntilDistance(distance, speed = 10, limit = 0):
    tank.on(speed, speed)
    count = 0
    while us.value() > distance:
        count += 1
        if(limit != 0 and count > limit):
            return False
        pass
    tank.stop()
    return True

def walkUntilColor(color, speed = 10, limit = 0):
    tank.on(speed, speed)
    count = 0
    while Sensor_Cor[0].value() != color and Sensor_Cor[1].value() != color:
        count += 1
        if(limit != 0 and count > limit):
            return False
        pass
    tank.stop()
    return True

def grabTube():
    #fica se mexendo
    rotateTo(10)

    for i in range(0, 2):
        rotateTo(-20, speed = 5 , linearSpeed = 5)
        rotateTo(20, speed = 5, linearSpeed = 5)

        if(us.value() < 80):
            break

    rotateTo(-10)
    #avança para pegar o tubo

    #retorna se pegou ou não
    if(us.value() < 80):
        tank.on_for_degrees(10, 10, 90)
        return True

    return False

def alignWithTube(degrees, count = 0, test = True):
    if(count == 5):
        tank.on_for_degrees(10, 10, -100 * count)
        backOriginalPosition(0)
        main()
        return "break"

    tube = {
        "angle": 0,
        "dist": 500
    }

    loopSize = int(degrees/5)
    loopCal = int(loopSize/2)

    startAngle = gy.value()

    for i in range(0, loopSize):
        ultra = us.value() if us.value() < 500 else 500

        # fazer ele se mecher e ler diversar distancias dentro desse 10cm e  calcular a media
        if(ultra < tube['dist']):
            tube['angle'] = i*5 #Angulo Atual
            tube['dist'] = ultra

        if(i == loopCal): #recalibra
            rotateTo(startAngle + (degrees/2) - gy.value())

        rotateTo(5, speed = 4)


    rotateTo(-degrees)
    rotateTo(startAngle - gy.value())

    startAngle = gy.value()
    for i in range(0, loopSize):
        ultra = us.value() if us.value() < 500 else 500

        # fazer ele se mecher e ler diversar distancias dentro desse 10cm e  calcular a media
        if(ultra < tube['dist']):
            tube['angle'] = i*-5 #Angulo Atual
            tube['dist'] = ultra

        if(i == loopCal): #recalibra
            rotateTo(startAngle - (degrees/2) - gy.value())

        rotateTo(-5 , speed = 4)

    # agora ja sei o angulo onde o tubo de encontra
    rotateTo(degrees)
    rotateTo(startAngle - gy.value())

    if(tube['dist'] == 500 and test):
        tank.on_for_degrees(10, 10, 180)
        alignWithTube(90, count + 1)
        return True;

    if tube['dist'] == 500 and not test:
        tank.on_for_degrees(10, 10, -180)
        alignWithTube(60, count + 1)
        return True

    rotateTo(tube['angle'])
    return tube['angle'];

def backOriginalPosition(baseAngle):
    walkUntilDistance(2000, speed = -10, limit = 1500)
    rotateTo(180)
    rotateTo(-baseAngle)

    walkUntilColor(1)
    alinhar(1)
    rotateTo(180)
    walkUntilColor(1)
    alinhar(1)

def PegarTubo():
    # Rotaciona e acha o angulo onde o tubo se encontra
    tank.on_for_degrees(10, 10, 180)
    baseAngle = alignWithTube(90, count = 1)
    if(baseAngle == "break"):
        return True

    # # Caminha até o tubo
    if (not walkUntilDistance(110, limit = 1500)):#10cm

        if(us.value() < 200):
            tank.on_for_degrees(10, 10, 90)
        else:
            tank.on_for_degrees(10, 10, -120)
            baseAngle += alignWithTube(40, test = False)
            tank.on_for_degrees(10, 10, 120)
    #caminha mais um pouco com a intenção de empurrar um pouco o tubo
    tank.on_for_degrees(10, 10, 45)

    for i in range (0,2):
        if(grabTube()):
            break

    if(us.value() < 80):
        Mov_Garra_Sensor(0, 150)
        tank.on_for_degrees(10, 10, -360)
        rotateTo(180)
        rotateTo(-baseAngle)

        walkUntilColor(1)
        alinhar(1)
    else:
        tank.on_for_degrees(10, 10, -360)
        backOriginalPosition(baseAngle)
        main()

    return True
