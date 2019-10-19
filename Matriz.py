#!/usr/bin/env python3
import termios, tty, sys
from ev3dev.ev3 import *
from threading import *

import time
import math

m2 = LargeMotor('outD')
m1 = LargeMotor('outC')

ir = UltrasonicSensor('in4')
ir.mode = 'US-DIST-CM'

gy = GyroSensor('in1')
gy.mode = 'GYRO-ANG'

us = UltrasonicSensor('in2')
us.mode = 'US-DIST-CM'

matriz_gasoduto = []
matriz_cano = []

linha = []
for i in range(31):
    linha.append(1)
matriz_gasoduto.append(linha)

linha = []
for i in range(31):
    linha.append(0)
matriz_gasoduto.append(linha)

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
                        speed1 = self.vel - 20
                    elif g < angulo_base:
                        speed2 = self.vel - 20
                    else:
                        speed1, speed2 = self.vel, self.vel
                    m1.run_forever(speed_sp=speed1)
                    m2.run_forever(speed_sp=speed2)
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")

                self.andando = False
                self.parando = False
                self.ang = 0.2

    def andar(self, speed = 200, angulo = 0.2):
        self.andando = True
        self.vel = speed
        self.ang = angulo

    def parar(self):
        self.parando = True

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

#9 quadrados
def anda(tamanho):
    print("andei")
    m2.run_to_rel_pos(position_sp=(180*(tamanho)),speed_sp=180,stop_action="brake")
    m1.run_to_rel_pos(position_sp=(180*(tamanho)),speed_sp=180,stop_action="brake")
    time.sleep(5)
def ondeTo(andeiLinha,andeiColuna, linha_inicio, coluna_inicio):
    linha_inicio = linha_inicio +andeiLinha
    coluna_inicio = coluna_inicio +andeiColuna
    return linha_inicio,coluna_inicio

def Ir_Pos_Matriz(pIni, pFim, angulo):
    tempo_andar = time.time()
    print("entrou aq", pIni, pFim)
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

def Entregar_Tubo(p1 = -1, p2 = 0, angulo = 0):
    lego.parar()
    tempo_t, medio_t = 0, 0
    if p1 == -1:
        while True:
            if ir.value() < 150:
                if tempo_t == 0:
                    lego.andar(speed=-100, angulo=angulo)
                else:
                    lego.parar()
                    medio_t = (time.time() - tempo_t)/2
                    break
            else:
                if tempo_t == 0:
                    tempo_t = time.time()
                    lego.andar(speed=-100, angulo=angulo)
    else:
        print("entrega especial")
        tempo_t = time.time()
        Ir_Pos_Matriz(p1, p2, angulo)
        medio_t = (time.time() - tempo_t) / 2

    print(medio_t)
    m1.run_timed(time_sp = 1000*medio_t, speed_sp = 100, stop_action="brake")
    m2.run_timed(time_sp = 1000*medio_t, speed_sp = 100, stop_action="brake")
    time.sleep(medio_t+1)
    #gyro(-90)
    print("Colocando tubo....")
    time.sleep(3)
    #gyro(90)
    while ir.value() > 150:
        m1.run_forever(speed_sp = 100)
        m2.run_forever(speed_sp = 100)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")

def tamanhoCano(tamanho):
    print("tempo do tamanho: ", tamanho)
    if tamanho < 1.5 :
        return 10
    elif tamanho < 2.5:
        return 15
    return 20

def scan_gasoduto(tam_tubo):
    com_tubo, primeiro = tam_tubo, [False, 0]
    passos, passos_ant, passos_ant2 = -1, 0, 0
    tempinho, tempo_andar, espaco = 0, 0, 0
    vao, vao_tubo = False, 0
    angulo_inicial = gy.value()

    while True:
        us_value = us.value()
        ir_value = ir.value()
        #Abaixo está a detecção do gasoduto
        if us_value > 150 and vao == False: #Descobre um vao
            print("Inicio vao")
            matriz_gasoduto[1][passos] = 1
            tempinho = time.time()
            passos_ant = passos
            vao = True
        elif vao and us_value < 150: #Vao fechou
            if (time.time() - tempinho) < 0.5:
                matriz_gasoduto[1][passos_ant] = 0
                print("vao falso")
            else:
                print("fim vao")
            vao = False

        #Verificar se ja detectou alguma vez:
        if not primeiro[0] and (ir_value < 150 or (vao and ir_value < 410)):
            primeiro[0] = True
            
        #Abaixo está a detecção dos canos no gasoduto
        if ir_value > 150 and vao_tubo == 0: #Descobre um vao de tubo
            if vao:
                if ir_value > 410:
                    print("Inicio tubo 2")
                    matriz_gasoduto[1][passos] = 2
                    vao_tubo = 1
                    passos_ant2 = passos
            else:
                print("Inicio tubo")
                if matriz_gasoduto[0][passos] == 0:
                    matriz_gasoduto[0][passos] = 2
                    passos_ant2 = passos
                else:
                    matriz_gasoduto[0][passos+1] = 2
                    passos_ant2 = passos + 1

                if not primeiro[0]:
                    primeiro[1] = time.time()
                    matriz_gasoduto[0][passos] = 2

                vao_tubo = 2

            espaco = time.time()

        elif vao_tubo != 0: #Vao de tubo fechou
            if vao_tubo == 1:
                if (time.time() - espaco) >= 3:
                    matriz_gasoduto[1][passos_ant2] = [2, tamanhoCano(time.time() - espaco)]
                    Entregar_Tubo(p1=passos, p2=passos_ant2, angulo=angulo_inicial)
                    vao_tubo = 0
                if ir_value < 410 or not vao:
                    if (time.time() - espaco) < 0.7:
                        print("tubo falso")
                        matriz_gasoduto[1][passos_ant2] = 0
                    else:
                        print("Fim tubo 2")
                        matriz_gasoduto[1][passos_ant2] = [2, tamanhoCano(time.time() - espaco)]
                    vao_tubo = 0
            elif vao_tubo == 2:
                if (time.time() - espaco) >= 3:
                    matriz_gasoduto[0][passos_ant2] = [2, tamanhoCano(time.time() - espaco)]
                    Entregar_Tubo(p1=passos, p2=passos_ant2, angulo=angulo_inicial)
                    vao_tubo = 0
                if ir_value < 150 or vao:
                    if (time.time() - espaco) < 0.7:
                        print("%.2f" %(time.time() - espaco))
                        print("tubo falso")
                        matriz_gasoduto[0][passos_ant2] = 0
                    else:
                        print("%.2f" %(time.time() - espaco))
                        print("Fim tubo")

                        t_tubo = tamanhoCano(time.time() - espaco)
                        matriz_gasoduto[0][passos_ant2] = [2, tamanhoCano(time.time() - espaco)]
                        print(matriz_gasoduto)            

                        if com_tubo <= t_tubo:
                            Entregar_Tubo(angulo=angulo_inicial)
                            #com_tubo = 30 #largou o tubo
                    vao_tubo = False

        #Andar pela matriz
        if passos < 31 and (time.time() - tempo_andar) > 0.85:
            lego.andar(speed = 150, angulo = angulo_inicial)
            passos += 1
            tempo_andar = time.time()
            #verificar leitura sensores de queda.
        else:
            if passos > 30:
                return 0
  
while(True):
    time.sleep(1)
    tempo = scan_gasoduto(10)
    print("tempo: %d" %tempo)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(10)
  