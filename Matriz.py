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

balanco = 0

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
        #teste:
        global balanco
        while True:
            if self.andando:
                #angulo_base = gy.value()
                #if self.ang != 0.2:
                #    angulo_base = self.ang
                speed1, speed2 = self.vel, self.vel
                while self.parando == False:
                    #g = gy.value()
                    #if balanco > angulo_base:
                    #    speed1 = self.vel - 0
                    #elif g < angulo_base:
                    #    speed2 = self.vel - 0
                    #else:
                    #    speed1, speed2 = self.vel, self.vel
                    if balanco < 0:
                        speed1 += balanco
                        balanco = 0
                    elif balanco > 0:
                        speed2 -= balanco
                        balanco = 0
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
        if self.andando:
            self.parando = True
            self.parado = True

    def andar_tempo(self, speed = 200, angulo = 0.2, tempo = 0):
        self.parar()
        while self.parado:
            pass
        t = time.time()
        while (time.time() - t) <= tempo:
            self.andar(speed=speed)
        self.parar()

lego = andar()
lego.daemon = True
lego.start()

#teste
class mostrar(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global balanco
        while True:
            k = getch()

            if k == 'd':
                balanco = 10
            elif k == 'a':
                balanco = -10
            elif k == 'q':
                exit()
            time.sleep(0.2)

p = mostrar()
p.daemon = True
p.start()

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

def Testar_Dist(virar = True):
    lego.parar()
    if virar:
        Girar(-90)
    valores = []
    somar = 0
    for i in [-10, 5, 5, -5]:
        u = us2.value()
        print(u)
        valores.append(u)
        somar += u
        Girar(i)

    if all(i > 2300 for i in valores) or all(i < 2300 for i in valores):
        if virar:
            Girar(90)
        print("t_dist 1: ", (somar / int(len(valores))))
        return (somar / int(len(valores)))
    else:
        somar = [0, 0]
        for i in valores:
            if i < 2300:
                somar[0] += i
                somar[1] += 1
        if virar:
            Girar(90)
        print("t_dist 2: ", (somar[0] / somar[1]))
        return (somar[0] / somar[1])

def Arrumar_Angulo():
    m = -1
    while True:
        a = Testar_Dist(virar=False)
        lego.andar_tempo(speed=m*150, tempo=0.9)
        b = Testar_Dist(virar=False)
        print("primeiro: ", abs(b - a))
        if abs(b - a) < 3:
            break
        else:
            if m < 0:
                Girar((a - b))
                print("m < 0: ", (a - b))
            else:
                print("m > 0: ", (b - a))
                Girar((b - a))
        m *= -1
    if m > 1:
        lego.andar_tempo(speed=-150, tempo=0.9)
        return 0
    else:
        return 0

def c_tubo(tam_tubo):
    vao, vao_tubo = False, False
    #com_tubo = tam_tubo

    tempos = {
        "vao_baixo": 0,
        "matriz": 0,
        "vao_alto": 0
    }

    var = {
        "Estados": 0,
        "Tarefa": 0,
        "Distancia": 0,
        "L_Anterior": 0
    }

    while True:
        us_value = int(us.value())
        us2_value = int(us2.value())

        if var['Estados'] == 0:
            tempos['matriz'] = 0
            if var['Tarefa'] == 0:
                u = Testar_Dist()

                t = time.time()
                while u > 2500:
                    if (time.time() - t) > 15:
                        t = time.time()
                        lego.andar(speed=150)
                        while (time.time() - t) < 3:
                            pass
                            #verificar se nao ta caindo
                        lego.parar()
                        t = time.time()
                    u = Testar_Dist()

                lego.andar(speed=150)
                t = time.time()
                while u > 0:
                    if (time.time() - t) > 1:
                        u -= 30
                        t = time.time()
                
                lego.andar_tempo(speed=-150, tempo=2.5)
                Girar(-90)
                u = Testar_Dist()
                var['Distancia'] = u
                var['Estados'] = 1

            elif var['Tarefa'] == 1:
                lego.andar_tempo(speed=-150, tempo=2)
                Girar(-90)
                u = Testar_Dist(virar=False)
                while True:
                    lego.andar(speed=150)
                    lt = us2.value()
                    if lt < 2540:
                        if (lt - u) > 20:
                            break
                    else:
                        u2 = Testar_Dist(virar=False)
                        if (u2 - u) > 20:
                            break
                lego.andar_tempo(speed=150, tempo=2)
                Girar(90)
                lego.andar_tempo(speed=150, tempo=2)
                u = Testar_Dist()
                var['Distancia'] = u
                var['Estados'] = 1
                var['Tarefa'] = 0
            
            #var['L_Anterior'] = Testar_Dist(virar=False)
            tempos['matriz'] = time.time()
            lego.andar(speed = 150)

        elif var['Estados'] == 1:
            #Andar
            us_value = int(us.value())
            us2_value = int(us2.value())
            if us2_value > 2549:
                continue
            if (time.time() - tempos['matriz']) > 0.3 and var['Distancia'] > 0:
                lego.andar(speed = 150)
                var['Distancia'] -= 10
                print(us2_value)
                #verificar leitura sensores de queda.
                if False: #por hora
                    return 0
                '''
                if var['L_Anterior'] != 0:
                    if abs(Testar_Dist(virar=False) - var['L_Anterior']) > 10:
                        var['Distancia'] += 30
                        Arrumar_Angulo()
                    else:
                        tempos['matriz'] = time.time()
                else:
                    tempos['matriz'] = time.time()
                '''
                tempos['matriz'] = time.time()
            else: 
                if var['Distancia'] <= 0:
                    lego.parar()
                    var['Estados'] = 0
                    var['Tarefa'] = 1
                    #verificar se ta detectando um espaco na tubulacao pra por cano e se cabe o cano q ta segurando
                    continue

            #Abaixo está a detecção do gasoduto ------------------------------------------------------------------
            if 200 < us2_value < 2500 and vao == False: #Descobre um vao
                print("Inicio vao", us2_value)
                tempos['vao_baixo'] = time.time()
                vao_tubo = False
                vao = True

            elif vao and (us2_value < 200 or (time.time() - tempos['vao_baixo']) > 2): #Vao fechou
                if (time.time() - tempos['vao_baixo']) < 1.1 or us2_value < 200:
                    print("vao falso: ", (time.time() - tempos['vao_baixo']))
                    vao = False
                else:
                    print("fim vao")
                    Girar(90)
                    var['Estados'] = 0
                    vao = False
                    continue
                
            #Abaixo está a detecção dos canos no gasoduto --------------------------------------------------------
            if us_value > 150 and not vao_tubo and not vao: #Descobre um vao de tubo
                print("Inicio tubo", us_value)
                vao_tubo = True
                tempos['vao_alto'] = time.time()

            elif vao_tubo: #Vao de tubo fechou
                if (time.time() - tempos['vao_alto']) >= 3:
                    print("fim tubo por tempo", (time.time() - tempos['vao_alto']))
                    print((time.time() - tempos['vao_alto']))
                    Entregar_Tubo(tempo=(time.time() - tempos['vao_alto']))
                    vao_tubo = False

                elif us_value < 150:
                    if (time.time() - tempos['vao_alto']) > 1.1:
                        print("fim tubo", (time.time() - tempos['vao_alto']))
                        Entregar_Tubo(tempo=(time.time() - tempos['vao_alto']))
                    vao_tubo = False

time.sleep(1)
tempo = c_tubo(10)
print("acabou")
time.sleep(10)