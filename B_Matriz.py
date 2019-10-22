#!/usr/bin/env python3
#coding: utf-8
import termios, tty, sys
from ev3dev.ev3 import *
from threading import *

import time
import math

m1 = LargeMotor('outA')
m2 = LargeMotor('outD')
m3 = MediumMotor('outB') #Motor mais alto
m4 = MediumMotor('outA') #Motor mais baixo

us = UltrasonicSensor('in3')
us.mode = 'US-DIST-CM'

gy = GyroSensor('in1')
gy.mode = 'GYRO-ANG'

us2 = UltrasonicSensor('in2')
us2.mode = 'US-DIST-CM'
'''
ir2 = InfraredSensor('in3')
ir2.mode = 'IR-PROX'
'''
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    ch = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch

class andar(Thread):
    def __init__(self):
        self.andando = False
        self.parando = False
        self.vel = 200
        self.ang = 0.2
        self.parado = False
        Thread.__init__(self)

    def run(self):
        global gy
        while True:
            if self.andando:
                angulo_base = gy.value()
                if self.ang != 0.2:
                    angulo_base = self.ang
                speed1, speed2 = self.vel, self.vel
                while self.parando == False:
                    g = gy.value()
                    if g > angulo_base:
                        speed1 = self.vel - 0
                    elif g < angulo_base:
                        speed2 = self.vel - 0
                    else:
                        speed1, speed2 = self.vel, self.vel
                    m1.run_forever(speed_sp=speed1)
                    m2.run_forever(speed_sp=speed2)
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")

                self.andando = False
                self.parando = False
                self.ang = 0.2
                self.parado = False

    def andar(self, speed = 200, angulo = 0.2):
        while self.parado:
            pass
        self.andando = True
        self.parando = False
        self.vel = speed
        self.ang = angulo

    def parar(self):
        self.parando = True
        self.parado = True

    def andar_tempo(self, speed = 200, angulo = 0.2, tempo = 0):
        t = time.time()
        while (time.time() - t) <= tempo:
            self.andar(speed=speed)
        self.parar()

lego = andar()
lego.daemon = True
lego.start()

'''
class Communication(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            k = getch()
            if k == 'p':
                lego.parar()
                exit()
                quit()
            
Comm = Communication()
Comm.daemon = True
Comm.start()
'''

def Ir_Pos_Matriz(pIni, pFim, angulo): #testar em outro arquivo..
    tempo_andar = time.time()
    while True:
        if pIni == pFim:
            return 0
        elif pIni < pFim:
            if pIni < pFim and (time.time() - tempo_andar) > 0.85:
                lego.andar(speed = 150, angulo = angulo)
                pIni += 1
                tempo_andar = time.time()
            else:
                if pIni == pFim:
                    return 0
        else:
            if pIni > pFim and (time.time() - tempo_andar) > 0.85:
                lego.andar(speed = -150, angulo = angulo)
                pIni -= 1
                tempo_andar = time.time()
            else:
                if pIni == pFim:
                    return 0

def Girar(ang):
    atual = gy.value()
    if ang > 0:
        ang -= 3
        while abs(gy.value() - atual) < abs(ang):
            m1.run_forever(speed_sp=100)
            m2.run_forever(speed_sp=-100)
    else:
        ang += 3
        while abs(gy.value() - atual) < abs(ang):
            m1.run_forever(speed_sp=-100)
            m2.run_forever(speed_sp=100)
    
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")

def Mov_Garra_Analog(Sentido, Pos): 
    if Sentido:
        m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
        time.sleep(1)
    else:
        m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
        time.sleep(1)

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

def Cano_Suporte(pos):
    Mov_Garra_Analog(1, 100)
    Para_Motor_Large(600)
    time.sleep(2)
    Mov_Garra_Analog(0, 180)

    m1.run_to_rel_pos(position_sp=-pos,speed_sp=250,stop_action="brake")
    m2.run_to_rel_pos(position_sp=-pos,speed_sp=250,stop_action="brake")
    time.sleep(2)

def Entregar_Tubo(angulo = 0, tempo = 0):
    lego.parar()
    lego.andar_tempo(speed=-150, tempo=tempo)
    #Girar(90)
    print("colocando o tubo")
    #Cano_Suporte(200)
    #Girar(-90)
    lego.andar_tempo(speed=150, tempo=tempo)

def c_tubo(tam_tubo):
    vao, vao_tubo = False, 0
    com_tubo = tam_tubo

    tempos = {
        "vao_baixo": 0,
        "vao_baixo_2": 0,
        "matriz": 0,
        "vao_alto": 0
    }

    while True:
        us_value = us.value()
        us2_value = us2.value()

        #Andar pela matriz
        if (time.time() - tempos['matriz']) > 0.9:
            lego.andar(speed = 150)
            tempos['matriz'] = time.time()
            #verificar leitura sensores de queda.
            if False: #por hora
                return 0

        #Abaixo está a detecção do gasoduto ------------------------------------------------------------------
        if (us2_value > 150 and vao == False) or us2_value > 300: #Descobre um vao
            if us2_value > 500:
                print("Inicio vao 2", us2_value)
                tempos['vao_baixo_2'] = time.time()
            else:
                print("Inicio vao", us2_value)
            tempos['vao_baixo'] = time.time()
            vao = True

        elif (vao and us2_value < 150) or (tempos['vao_baixo'] != 0 and us2_value < 500): #Vao fechou
            if (time.time() - tempos['vao_baixo']) < 0.5 or (time.time() - tempos['vao_baixo_2']) < 0.5:
                print("vao falso: ", (time.time() - tempos['vao_baixo']), (time.time() - tempos['vao_baixo_2']))
            else:
                if tempos['vao_baixo_2'] != 0:
                    print("fim vao 2 ", ((time.time() - tempos['vao_baixo_2'])*(2/3)))
                    lego.andar_tempo(speed=-150, tempo=((time.time() - tempos['vao_baixo_2'])*(2/3)))
                    Girar(90)
                    lego.andar_tempo(speed=150, tempo=2)
                    Girar(-90)
                    tempos['vao_baixo_2'] = 0
                else:
                    print("fim vao")
            vao = False
            
        #Abaixo está a detecção dos canos no gasoduto --------------------------------------------------------
        if us_value > 150 and vao_tubo == 0: #Descobre um vao de tubo
            if vao:
                if us_value > 410:
                    print("Inicio tubo 2", us_value)
                    vao_tubo = 1
            else:
                print("Inicio tubo", us_value)
                vao_tubo = 2

            tempos['vao_alto'] = time.time()

        elif vao_tubo != 0: #Vao de tubo fechou
            if vao_tubo == 1:
                print("vao_tubo 1", (time.time() - tempos['vao_alto']))
                if (time.time() - tempos['vao_alto']) >= 3:
                    Entregar_Tubo(tempo=(time.time() - tempos['vao_alto']))
                    vao_tubo = 0
                    
                if us_value < 410 or not vao or tempos['vao_baixo_2'] != 0:
                    if (time.time() - tempos['vao_alto']) > 1.1:
                        print("vao_tubo 1 ou ", vao, " ou ", tempos['vao_baixo_2'], (time.time() - tempos['vao_alto']))
                        Entregar_Tubo(tempo=(time.time() - tempos['vao_alto']))
                    vao_tubo = 0

            elif vao_tubo == 2:
                if (time.time() - tempos['vao_alto']) >= 3:
                    print("vao_tubo 2", (time.time() - tempos['vao_alto']))
                    print((time.time() - tempos['vao_alto']))
                    Entregar_Tubo(tempo=(time.time() - tempos['vao_alto']))
                    vao_tubo = 0

                if us_value < 150 or vao or tempos['vao_baixo_2'] != 0:
                    if (time.time() - tempos['vao_alto']) > 1.1:
                        print("vao_tubo 2 ou ", vao, " ou ", tempos['vao_baixo_2'], (time.time() - tempos['vao_alto']))
                        Entregar_Tubo(tempo=(time.time() - tempos['vao_alto']))
                    vao_tubo = 0

time.sleep(1)
tempo = c_tubo(10)
print("acabou")
time.sleep(10)