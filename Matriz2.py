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

balanco = [0, 0]

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
                    m1.run_forever(speed_sp=(speed1+0))
                    m2.run_forever(speed_sp=(speed2+0))
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

def rotateTo(ang):
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

'''

def Testar_Dist():
    lego.parar()
    valores = []
    somar = 0
    for i in [1, -1, 1, -1]:
        u = Comm.us2_value
        print(u)
        valores.append(u)
        somar += u
        lego.andar_tempo(speed=(i*200), tempo=0.3)
        time.sleep(0.3)

    if all(i > 2300 for i in valores) or all(i < 2300 for i in valores):
        print("t_dist 1: ", (somar / int(len(valores))))
        return (somar / int(len(valores)))
    else:
        somar = [0, 0]
        for i in valores:
            if i < 2300:
                somar[0] += i
                somar[1] += 1
        print("t_dist 2: ", (somar[0] / somar[1]))
        return (somar[0] / somar[1])

'''

def Entregar_Tubo(angulo = 0, tempo = 0, tam=0):
    lego.parar()
    if tam < 20:
        lego.andar_tempo(speed=-150, tempo=(tempo - 1))
    else:
        lego.andar_tempo(speed=-150, tempo=(tempo - 2))
    rotateTo(90)
    print("colocando o tubo")
    Cano_Suporte(200)
    rotateTo(-90)
    lego.andar_tempo(speed=150, tempo=tempo)

def Testar_Dist(virar = True):
    lego.parar()
    if virar:
        rotateTo(-90)
    valores = []
    somar = 0
    for i in [-10, 5, 5, -5]:
        u = Comm.us2_value
        print(u)
        valores.append(u)
        somar += u
        rotateTo(i)

    if all(i > 2300 for i in valores) or all(i < 2300 for i in valores):
        if virar:
            rotateTo(90)
        print("t_dist 1: ", (somar / int(len(valores))))
        return (somar / int(len(valores)))
    else:
        somar = [0, 0]
        for i in valores:
            if i < 2300:
                somar[0] += i
                somar[1] += 1
        if virar:
            rotateTo(90)
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
                rotateTo((a - b))
                print("m < 0: ", (a - b))
            else:
                print("m > 0: ", (b - a))
                rotateTo((b - a))
        m *= -1
    if m > 1:
        lego.andar_tempo(speed=-150, tempo=0.9)
        return 0
    else:
        return 0

def c_tubo(tam_tubo):
    global balanco
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
        "L_Anterior": 0,
        "Trava": 0
    }

    cascata = [0, 0, 0]
    temp = 0
    leituras = []
    fim = False
    re = False

    ant = Comm.us2_value
    while ant > 1000:
        ant = Testar_Dist(virar=False)
    while True:
        us_value = int(Comm.us_value)
        us2_value = int(Comm.us2_value)
        if us2_value > 2549:
            continue

        #Abaixo está a detecção do gasoduto ------------------------------------------------------------------
        if 200 < us2_value < 2500 and vao == False: #Descobre um vao
            print("Inicio vao", us2_value)
            tempos['vao_baixo'] = time.time()
            vao_tubo = False
            vao = True
            re = True

        elif vao and us2_value < 200 or fim: #Vao fechou
            if (time.time() - tempos['vao_baixo']) > 1.1:
                print("fim vao")
                if cascata[0] != 0:
                    cascata[1] = (time.time() - tempos['vao_baixo']) + 1
                else:
                    cascata[0] = (time.time() - tempos['vao_baixo']) + 1
                temp = time.time()
                lego.andar_tempo(speed=-150, tempo=((time.time() - tempos['vao_baixo']) - 1))
                rotateTo(90)
                lego.andar_tempo(speed=150, tempo = 2)
                rotateTo(-90)
                vao_tubo = False
                vao = False
                re = False
                ant = Comm.us2_value
                while ant > 1000:
                    ant = Testar_Dist(virar=False)
            else:
                print("vao falso: ", (time.time() - tempos['vao_baixo']))
                vao = False
                re = False
            if fim:
                if vao:
                    if cascata[0] != 0:
                        print("fim sem conseguir")
                        lego.andar_tempo(speed=-150, tempo=3)
                        return 0
                    else:
                        if (time.time() - tempos['vao_baixo']) > 1.1:
                            print("fim vao")
                            if cascata[0] != 0:
                                cascata[1] = (time.time() - tempos['vao_baixo']) + 1
                            else:
                                cascata[0] = (time.time() - tempos['vao_baixo']) + 1
                            temp = time.time()
                            lego.andar_tempo(speed=-150, tempo=((time.time() - tempos['vao_baixo']) - 1))
                            rotateTo(90)
                            lego.andar_tempo(speed=150, tempo = 2)
                            rotateTo(-90)
                            vao_tubo = False
                            vao = False
                            re = False
                            ant = Comm.us2_value
                            while ant > 1000:
                                ant = Testar_Dist(virar=False)
                        else:
                            print("fim sem conseguir 2")
                else:
                    print("fim sem conseguir 3")
                    lego.andar_tempo(speed=-150, tempo=3)
                    return 0

        elif vao:
            leituras.append(us2_value)
            if (time.time() - tempos['vao_baixo']) > 0.5:
                somatorio = 0
                for i in range(len(leituras)):
                    somatorio += leituras[i]
                somatorio /= int(len(leituras))
                ant = somatorio
                re = False

        #Abaixo está a detecção dos canos no gasoduto --------------------------------------------------------
        if us_value > 200 and not vao_tubo: #Descobre um vao de tubo
            print("Inicio tubo", us_value)
            vao_tubo = True
            tempos['vao_alto'] = time.time()

        elif vao_tubo or var['Trava'] != 0: #Vao de tubo fechou
            if ((time.time() - tempos['vao_alto']) >= 3) and (not vao or var['Trava'] == 2):
                print("fim tubo por tempo", (time.time() - tempos['vao_alto']))
                print((time.time() - tempos['vao_alto']))
                Entregar_Tubo(tempo=(time.time() - tempos['vao_alto']), tam=tam_tubo)
                return 1

            elif us_value < 200 and (not vao or var['Trava'] == 2):
                if (time.time() - tempos['vao_alto']) > 1.1:
                    if var['Trava'] == 3:
                        lego.andar_tempo(speed=-150, tempo=((time.time() - tempos['vao_alto'])+1))
                        var['Distancia'] += ((time.time() - tempos['vao_alto'])+1) * 30
                        print("fim vao com trava")
                        tempos['matriz'] = 0
                    else:
                        print("fim tubo", (time.time() - tempos['vao_alto']))
                        Entregar_Tubo(tempo=(time.time() - tempos['vao_alto']), tam=tam_tubo)
                        return 1
                vao_tubo = False
                var['Trava'] = 0

        #andar em uma linha reta se guiando pelo ultrasonic: ant é o valor q eu quero de distancia entre o brick e o gasoduto
        if cascata[0] == 0:
            lego.andar(speed=150)
        elif cascata[1] == 0:
            if (time.time() - temp) <= cascata[0]:
                lego.andar(speed=150)
            else:
                lego.andar_tempo(speed=-150, tempo=2)
                rotateTo(-90)
                lego.andar_tempo(speed=150, tempo=3.5)
                rotateTo(90)
                lego.andar_tempo(speed=150, tempo=1)
                cascata[0] = 0
        else:
            if (time.time() - temp) <= cascata[1]:
                lego.andar(speed=150)
            else:
                lego.andar_tempo(speed=-150, tempo=2)
                rotateTo(-90)
                lego.andar_tempo(speed=150, tempo=3.5)
                rotateTo(90)
                lego.andar_tempo(speed=150, tempo=1)
                cascata[1] = 0

        if not re:
            if (us2_value - ant) > 2:
                if (us2_value - ant) > 5:
                    balanco[0] = 15
                else:
                    balanco[0] = 10
            elif (us2_value - ant) < -2:
                if (us2_value - ant) < -5:
                    balanco[1] = 15
                else:
                    balanco[1] = 10
            else:
                balanco = [0, 0]
        else:
            balanco = [0, 0]
        if not fim:
            lego.andar(speed=150)

        if us.value() > 100 or us2.value() > 100:
            fim = True
            lego.parar()

time.sleep(1)
c_tubo(10)
print("acabou")
time.sleep(10)