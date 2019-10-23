#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *

from threading import *
from ev3dev2.motor import OUTPUT_C, OUTPUT_D, MoveTank
import time, socket, json
import math

tank = MoveTank(OUTPUT_D, OUTPUT_C)
m1 = LargeMotor('outD') #Direito
m2 = LargeMotor('outC') # Esquerdo
m3 = MediumMotor('outB')
m4 = MediumMotor('outA')
us = UltrasonicSensor('in3') #Direto
us2 = UltrasonicSensor('in4') #esquerdo
gy = GyroSensor('in1')
us3 = UltrasonicSensor('in2')
#Sensor_Cor = [ColorSensor('in2'), ColorSensor('in1')] #2 = Esquerdo, 1 = Direito

us.mode = 'US-DIST-CM'
us2.mode = 'US-DIST-CM'
us3.mode = 'US-DIST-CM'
gy.mode = 'GYRO-ANG'
#Sensor_Cor[0].mode = 'COL-COLOR'
#Sensor_Cor[1].mode = 'COL-COLOR'

class Communication(Thread):
    def __init__(self):
        self.sc_value = 0
        self.sc2_value = 0
        Thread.__init__(self)

    def run(self):
        while True:
            #try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('169.255.168.150', 3572))
                s.listen()
                while True:
                    conn, addr = s.accept()
                    with conn:
                        while True:
                            data = conn.recv(1024)

                            if not data:
                                break

                            Sedex = 0
                            try:
                                Sedex = json.loads(data.decode())
                            except:
                                st = data.decode()
                                st = st[2, 3]
                                for i in range(len(st)):
                                    if st[i] == '}':
                                        Sedex = json.loads(st[0:i+1])
                                        break
                                        
                            self.sc_value = Sedex['sc']
                            self.sc2_value = Sedex['sc2']
            #except Exception as e:
             #   print(e)
              #  time.sleep(0.5)

Comm = Communication()
Comm.daemon = True
Comm.start()
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

def alinharP(c, Sentido, temp): #Essa função alinha o lego a uma cor especifica c.
    if Comm.sc_value == c and Comm.sc2_value == c:
        return 0
    while True:
        if Comm.sc_value == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while Comm.sc_value == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            #m1.run_forever(speed_sp=-150)
            m2.run_forever(speed_sp=100)
            while Comm.sc2_value != c:
                if Comm.sc2_value == 0:
                    return 1
                if Comm.sc_value != c:
                    m2.stop(stop_action="brake")
                    m1.run_forever(speed_sp=70)
                else:
                    m1.stop(stop_action="brake")
                    m2.run_forever(speed_sp=100)
                '''if 40 < us2.value() < 400:
                    return 2'''
            break

        if Comm.sc2_value == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while Comm.sc2_value == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            m1.run_forever(speed_sp=100)
            #m2.run_forever(speed_sp=-150)
            while Comm.sc_value != c:
                if Comm.sc_value == 0:
                    return 1
                if Comm.sc2_value != c:
                    m1.stop(stop_action="brake")
                    m2.run_forever(speed_sp=70)
                else:
                    m1.run_forever(speed_sp=100)
                    m2.stop(stop_action="brake")
                '''if 40 < us.value() < 400:
                    return 1'''
            break
    m1.run_forever(speed_sp=Sentido)
    m2.run_forever(speed_sp=Sentido)
    time.sleep(temp)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(1)
    return 0

def alinhar(c): #Essa função alinha o lego a uma cor especifica c.
    if Comm.sc_value == c and Comm.sc2_value == c:
        return 0
    while True:
        if Comm.sc_value == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while Comm.sc_value == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            #m1.run_forever(speed_sp=-150)
            m2.run_forever(speed_sp=100)
            while Comm.sc2_value != c:
                if Comm.sc2_value == 0:
                    return 1
                if Comm.sc_value != c:
                    m2.stop(stop_action="brake")
                    m1.run_forever(speed_sp=70)
                else:
                    m1.stop(stop_action="brake")
                    m2.run_forever(speed_sp=100)
                if 70 < us2.value() < 400:
                    return 2
            break

        if Comm.sc2_value == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while Comm.sc2_value == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            m1.run_forever(speed_sp=100)
            #m2.run_forever(speed_sp=-150)
            while Comm.sc_value != c:
                if Comm.sc_value == 0:
                    return 1
                if Comm.sc2_value != c:
                    m1.stop(stop_action="brake")
                    m2.run_forever(speed_sp=70)
                else:
                    m1.run_forever(speed_sp=100)
                    m2.stop(stop_action="brake")
                if 70 < us.value() < 400:
                    return 1
            break

    m1.run_forever(speed_sp=250)
    m2.run_forever(speed_sp=250)
    time.sleep(1)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    return 0


def alinhar_ultra(): #Essa função alinha o lego a uma cor especifica c.
    if us.value() > 100 and us2.value() > 100:
        return 0
    if us.value() > 100:
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        while us.value() > 100:
            m1.run_forever(speed_sp=-50)
            m2.run_forever(speed_sp=-50)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        #m1.run_forever(speed_sp=-150)
        m2.run_forever(speed_sp=100)
        while us2.value() < 100:
            pass

    if us2.value() > 100:
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        while us2.value() > 100:
            m1.run_forever(speed_sp=-50)
            m2.run_forever(speed_sp=-50)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        m1.run_forever(speed_sp=100)
        #m2.run_forever(speed_sp=-150)
        while us.value() < 100:
            pass

    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(1)
    return 0

def Mov_Garra_Sensor(Sentido, Pos): #0 = descer; 1 = subir;
    if Sentido: 
        if (us3.value() < 400):
            while (us3.value() < 100):
                m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    else: 
        while (us3.value() > 45):
                m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    time.sleep(2)


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
    while us3.value() > distance:
        count += 1
        if(limit != 0 and count > limit):
            return False
        pass
    tank.stop()
    return True

def walkUntilColor(color, speed = 10, limit = 0):
    tank.on(speed, speed)
    count = 0
    while Comm.sc_value != color and Comm.sc2_value != color:
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

        if(us3.value() < 80):
            break

    rotateTo(-10)
    #avança para pegar o tubo

    #retorna se pegou ou não
    if(us3.value() < 80):
        tank.on_for_degrees(10, 10, 90)
        return True

    return False

def alignWithTube(degrees, count = 0, test = True):
    if(count == 5):
        tank.on_for_degrees(10, 10, -100 * count)
        backOriginalPosition(0)
        PegarTubo()
        return "break"

    tube = {
        "angle": 0,
        "dist": 500
    }

    loopSize = int(degrees/5)
    loopCal = int(loopSize/2)

    startAngle = gy.value()

    for i in range(0, loopSize):
        ultra = us3.value() if us3.value() < 500 else 500

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
        ultra = us3.value() if us3.value() < 500 else 500

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
        return alignWithTube(90, count + 1)

    if tube['dist'] == 500 and not test:
        tank.on_for_degrees(10, 10, -180)
        return alignWithTube(60, count + 1)

    rotateTo(tube['angle'])
    return tube['angle']

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

        if(us3.value() < 200):
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

    if(us3.value() < 80):
        Mov_Garra_Sensor(1, 150)
        tank.on_for_degrees(10, 10, -360)
        rotateTo(180)
        rotateTo(-baseAngle)

        walkUntilColor(1)
        alinhar(1)
    else:
        tank.on_for_degrees(10, 10, -360)
        backOriginalPosition(baseAngle)
        PegarTubo()

    return True

while True:
    m1.run_forever(speed_sp=150)
    m2.run_forever(speed_sp=150)
    if (Comm.sc_value == 1) or (Comm.sc2_value == 1):
        alinharP(1, -250, 3)
        rotateTo(90)
        while (us.value() < 100) or (us2.value() < 100):
            m1.run_forever(speed_sp=150)
            m2.run_forever(speed_sp=150)
        alinhar_ultra()
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        m1.run_forever(speed_sp=-150)
        m2.run_forever(speed_sp=-150)
        time.sleep(5)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        rotateTo(-90)
        walkUntilColor(1)
        alinharP(1, 0, 1)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        PegarTubo()
        alinharP(1, 150, 3)
        rotateTo(-90)
        while (us.value() < 100):
            m1.run_forever(speed_sp=140)
            m2.run_forever(speed_sp=140)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        m1.run_to_rel_pos(position_sp=(-100),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=(-100),speed_sp=180,stop_action="brake")
        rotateTo(-90)
        while True :
            if (Comm.sc_value == 2) or (Comm.sc_value == 2):
                alinhar(2)
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                break
            m1.run_forever(speed_sp=140)
            m2.run_forever(speed_sp=140)
            if(us.value() > 100):
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
        break
    if (Comm.sc_value == 3) or (Comm.sc2_value == 3):
        alinharP(3, -250, 3)
        rotateTo(180)
    if (50 < us.value() > 70) or (50 < us.value() > 70):
        if (us.value() > 50):
            rotateTo(90)
        else:
            rotateTo(-90)
        while True:
            while (us.value() < 100) or (us2.value() < 100):
                m1.run_forever(speed_sp=150)
                m2.run_forever(speed_sp=150)
            alinhar_ultra()
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            m1.run_forever(speed_sp=-150)
            m2.run_forever(speed_sp=-150)
            time.sleep(5)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            rotateTo(-90)
            walkUntilColor(1)
            alinharP(1, 0, 1)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            PegarTubo()
            if alinharP(1, 150, 3) == 0:
                rotateTo(-90)
            while (us.value() < 100):
                m1.run_forever(speed_sp=140)
                m2.run_forever(speed_sp=140)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            m1.run_to_rel_pos(position_sp=(-100),speed_sp=180,stop_action="brake")
            m2.run_to_rel_pos(position_sp=(-100),speed_sp=180,stop_action="brake")
            rotateTo(-90)
            while True :
                if Comm.sc_value == 2 or Comm.sc_value == 2:
                    alinhar(2)
                    print("achei o azul")
                    m1.stop(stop_action="brake")
                    m2.stop(stop_action="brake")
                    break
                m1.run_forever(speed_sp=140)
                m2.run_forever(speed_sp=140)
                if(us.value() > 100):
                    m1.stop(stop_action="brake")
                    m2.stop(stop_action="brake")
            break