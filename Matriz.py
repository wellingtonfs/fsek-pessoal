#!/usr/bin/env python3
import termios, tty, sys
from ev3dev.ev3 import *
from threading import *
import time
import math

m1 = LargeMotor('outA')
m2 = LargeMotor('outD')

ir = UltrasonicSensor('in4')
ir.mode = 'US-DIST-CM'

tc = TouchSensor('in3')

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

for i in range(2):
    linha = []
    for j in range(31):
        linha.append(0)
    matriz_cano.append(linha)

class paralelo(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            k = getch()

            if k == 'p':
                print(matriz_gasoduto[0])
                print(matriz_gasoduto[1])
            elif k == 'q':
                break

pp = paralelo()
pp.daemon = True
pp.start()

def andar(tempo_and):
    t_i = time.time()
    angulo_base = gy.value()
    speed1, speed2 = 200, 200
    while (time.time() - t_i) <= tempo_and:
        g = gy.value()
        if g < angulo_base:
            speed1 = 180
        elif g > angulo_base:
            speed2 = 180
        else:
            speed1, speed2 = 200, 200
        m1.run_forever(speed_sp=speed1)
        m2.run_forever(speed_sp=speed2)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")

def giraRobo(graus, tempo = 2): #90 > 0: direita else: esquerda
    razaoRobo = 5.5 / 3.0
    if graus > 0:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=180,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=-(razaoRobo*(graus*-1)),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=(razaoRobo*(graus*-1)),speed_sp=180,stop_action="brake")
    if tempo != 0:
        time.sleep(tempo)

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

def Entregar_Tubo(v = False):
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    tempo_t, medio_t = 0, 0
    if not v:
        while True:
            if ir.value() < 150:
                if tempo_t == 0:
                    m1.run_forever(speed_sp = -100)
                    m2.run_forever(speed_sp = -100)
                else:
                    m1.stop(stop_action="brake")
                    m2.stop(stop_action="brake")
                    medio_t = (time.time() - tempo_t)/2
                    break
            else:
                if tempo_t == 0:
                    tempo_t = time.time()
        
        m1.run_timed(time_sp = 1000*medio_t, speed_sp = 100)
        m2.run_timed(time_sp = 1000*medio_t, speed_sp = 100)
        time.sleep(medio_t+1)
        giraRobo(-90)
        print("Colocando tubo....")
        time.sleep(3)
        giraRobo(90)
        while ir.value() > 150:
            m1.run_forever(speed_sp = 100)
            m2.run_forever(speed_sp = 100)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")

def scan_gasoduto():
    primeiro = True
    com_tubo = True
    anterior_leitura = 0
    passos, passos_ant = -1, 0
    speed1, speed2 = 200, 216
    tempinho, tempo_andar = time.time(), 0
    vao, vao_tubo = False, False
    while True:
        if (time.time() - tempinho) > 0.5:
            if primeiro:
                anterior_leitura = us.value()
                primeiro = False
            elif abs(us.value() - anterior_leitura) > 100 and vao == False: #Descobre um vao
                print("Inicio vao")
                if (us.value() - anterior_leitura) > 0: #entrou no vao
                    matriz_gasoduto[1][passos] = 1
                    matriz_gasoduto[0][passos] = 0
                    passos_ant = passos
                anterior_leitura = us.value()
                vao = True
            elif vao and (anterior_leitura - us.value()) > 100: #Vao fechou
                print("final vao")      
                print("%d - %d" %(passos_ant, passos+1))
                for i in range(passos_ant, passos + 1, 1):
                    matriz_gasoduto[1][i] = 1
                    matriz_gasoduto[0][i] = 0
                anterior_leitura = us.value()
                vao = False
                
            tempinho = time.time()

        if ir.value() > 150 and vao_tubo == False: #Descobre um vao de tubo
            if vao:
                if ir.value() > 410:
                    print("Inicio tubo 2")
                    vao_tubo = True
            else:
                print("Inicio tubo")
                vao_tubo = True
        elif vao_tubo: #Vao de tubo fechou
            if vao:
                if ir.value() < 410:
                    print("Fim tubo 2")
                    vao_tubo = False
            else:
                if ir.value() < 150:
                    print("Fim tubo")
                    vao_tubo = False
                    if com_tubo:
                        Entregar_Tubo()
                        com_tubo = False
        
        if passos < 31 and (time.time() - tempo_andar) > 1:
            m1.run_to_rel_pos(position_sp=160, speed_sp=speed1, stop_action="brake")
            m2.run_to_rel_pos(position_sp=160, speed_sp=speed2, stop_action="brake")
            passos += 1
            tempo_andar = time.time()
        else:
            if passos > 30:
                return 0
            

matriz=["0,0","0,1","0,2","0,3","0,4","0,5","0,6","0,7","0,8","0,9","0,10","0,11","0,12"],["1,0","1,1","1,2","1,3","1,4","1,5","1,6","1,7","1,8","1,9","1,10","1,11","1,12"], ["2,0","2,1","2,2","2,3","2,4","2,5","2,6","2,7","2,8","2,9","2,10","2,11","2,12"], ["3,0","3,1","3,2","3,3","3,4","3,5","3,6","3,7","3,8","3,9","3,10","3,11","3,12"],   ["4,0","4,1","4,2","4,3","4,4","4,5","4,6","4,7","4,8","4,9","4,10","4,11","4,12"], ["5,0","5,1","5,2","5,3","5,4","5,5","5,6","5,7","5,8","5,9","5,10","5,11","5,12"],["6,0","6,1","6,2","6,3","6,4","6,5","6,6","6,7","6,8","6,9","6,10","6,11","6,12"],  ["7,0","7,1","7,2","7,3","7,4","7,5","7,6","7,7","7,8","7,9","7,10","7,11","7,12"],["8,0","8,1","8,2","8,3","8,4","8,5","8,6","8,7","8,8","8,9","8,10","8,11","8,12"],["9,0","9,1","9,2","9,3","9,4","9,5","9,6","9,7","9,8","9,9","9,10","9,11","9,12"],["10,0","10,1","10,2","10,3","10,4","10,5","10,6","10,7","10,8","10,9","10,10","10,11","10,12"],["11,0","11,1","11,2","11,3","11,4","11,5","11,6","11,7","11,8","11,9","11,10","11,11","11,12"]
while(True):
    minha_posicao = 0
    linha_inicio = 10
    coluna_inicio = 10

    tempo = scan_gasoduto()
    print("tempo: %d" %tempo)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(10)