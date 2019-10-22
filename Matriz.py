#!/usr/bin/env python3
#coding: utf-8
import termios, tty, sys
from ev3dev.ev3 import *
from threading import *

import time
import math

m1 = LargeMotor('outC')
m2 = LargeMotor('outD')
m3 = MediumMotor('outB') #Motor mais alto
m4 = MediumMotor('outA') #Motor mais baixo

us = UltrasonicSensor('in2')
us.mode = 'US-DIST-CM'

gy = GyroSensor('in1')
gy.mode = 'GYRO-ANG'

ir = InfraredSensor('in4')
ir.mode = 'IR-PROX'
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
    #metade_tempo = tempo / 2
    t = time.time()
    while (time.time() - t) <= tempo:
        lego.andar(speed=-150)
    lego.parar()
    Girar(90)
    print("colocando o tubo")
    Cano_Suporte(200)
    Girar(-90)

def c_tubo(tam_tubo):
    #com_tubo= tam_tubo
    tempinho, tempo_andar, espaco = 0, 0, 0
    vao, vao_tubo = False, 0

    #ande até bater..
    #while ir2.value() > 3:
    #    lego.andar(speed=150)

    angulo_inicial = gy.value()
    keep_l = ir.value()

    while True:
        us_value = us.value()
        ir_value = ir.value()

        #corrigir angulo errado..
        if (keep_l - ir_value) < -3:
            angulo_inicial -= 3
            keep_l = ir_value
        elif (keep_l - ir_value) > 3:
            angulo_inicial += 3
            keep_l = ir_value

        #Andar pela matriz
        if (time.time() - tempo_andar) > 0.9:
            lego.andar(speed = 150, angulo = angulo_inicial)
            tempo_andar = time.time()
            #verificar leitura sensores de queda.
            if False: #por hora
                return 0

        #Abaixo está a detecção do gasoduto
        if 35 < ir_value < 100 and vao == False: #Descobre um vao
            print("Inicio vao")
            tempinho = time.time()
            vao = True
        elif vao and ir_value < 35: #Vao fechou
            if (time.time() - tempinho) < 0.5:
                print("vao falso")
            else:
                print("fim vao")
            vao = False
            
        #Abaixo está a detecção dos canos no gasoduto
        if us_value > 150 and vao_tubo == 0: #Descobre um vao de tubo
            if vao:
                if us_value > 410:
                    print("Inicio tubo 2")
                    vao_tubo = 1
            else:
                print("Inicio tubo")
                vao_tubo = 2

            espaco = time.time()

        elif vao_tubo != 0: #Vao de tubo fechou
            if vao_tubo == 1:
                print((time.time() - espaco))
                if (time.time() - espaco) >= 3:
                    Entregar_Tubo(angulo=angulo_inicial, tempo=(time.time() - espaco))
                    vao_tubo = 0
                    
                if us_value < 410 or not vao:
                    if (time.time() - espaco) > 1.1:
                        print((time.time() - espaco))
                        Entregar_Tubo(angulo=angulo_inicial, tempo=(time.time() - espaco))
                    vao_tubo = 0

            elif vao_tubo == 2:
                if (time.time() - espaco) >= 3:
                    print((time.time() - espaco))
                    Entregar_Tubo(angulo=angulo_inicial, tempo=(time.time() - espaco))
                    vao_tubo = 0

                if us_value < 150 or vao:
                    if (time.time() - espaco) > 1.1:
                        print((time.time() - espaco))
                        Entregar_Tubo(angulo=angulo_inicial, tempo=(time.time() - espaco))
                    vao_tubo = 0
        print(us_value)
    
while(True):
    time.sleep(1)
    tempo = c_tubo(10)
    print("tempo: %d" %tempo)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(10)