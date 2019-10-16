#!/usr/bin/env python3
from ev3dev.ev3 import *
import time
import math


m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
#cor = ColorSensor('in4')
#cor2 = ColorSensor('in1')
#us = UltrasonicSensor('in2')
#us2 = UltrasonicSensor('in3')
ir = InfraredSensor('in2')
ir.mode = 'IR-PROX'
#cor.mode = 'COL-COLOR'
#cor2.mode = 'COL-COLOR'
#us.mode = 'US-DIST-CM'
#us2.mode = 'US-DIST-CM'


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

def scan_gasoduto():
    tempo_inicio, tempos_pista, anterior_leitura = -1, [], 0
    tempo_dez, tempo_quinze, tempo_vinte = 0,0,0
    #if alinhar(3) == 0:
     #   m1.run_forever(speed_sp=150)
      #  m2.run_forever(speed_sp=150)
       # time.sleep(2)
        #m1.stop(stop_action="brake")
        #m2.stop(stop_action="brake")
        #giraRobo(-90)
    vao = False
    while True:

        m1.run_forever(speed_sp=50)
        m2.run_forever(speed_sp=50)
        print(ir.value())
        print(anterior_leitura)
       # time.sleep(20)
        
        # if us.value() > 38:
        #     m1.stop(stop_action="brake")
        #     m2.stop(stop_action="brake")
        #     giraRobo(180)
        #     if len(tempos_pista) > 1:
        #         tempos_pista.append(time.time())
        # if anterior_leitura == -1:
        #     print("no elif 1 ")
        #     tempos_pista.append(time.time()) 
        #     anterior_leitura = ir.value()
        #    time.sleep(1)
        if abs(ir.value() - anterior_leitura) > 15: #Descobre um vao
            print("no elif 2")
            tempos_pista.append(time.time())
            anterior_leitura = ir.value()
            time.sleep(4)
            if tempo_inicio == -1:
                print("dentro do if do elif 2")
                tempo_inicio = time.time()
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            time.sleep(5)       
            vao = True
        elif (vao == True) and ((abs(ir.value() - anterior_leitura)) > 15): #Vao fechou
            print("no elif 3")      
            tempos_pista.append(time.time())
            tempo_final = time.time()
            anterior_leitura = ir.value()
            print(tempo_final - tempo_inicio)
            vao = False
            time.sleep(4)
            return(tempo_final - tempo_inicio)
            #break        
        

matriz=["0,0","0,1","0,2","0,3","0,4","0,5","0,6","0,7","0,8","0,9","0,10","0,11","0,12"],["1,0","1,1","1,2","1,3","1,4","1,5","1,6","1,7","1,8","1,9","1,10","1,11","1,12"], ["2,0","2,1","2,2","2,3","2,4","2,5","2,6","2,7","2,8","2,9","2,10","2,11","2,12"], ["3,0","3,1","3,2","3,3","3,4","3,5","3,6","3,7","3,8","3,9","3,10","3,11","3,12"],   ["4,0","4,1","4,2","4,3","4,4","4,5","4,6","4,7","4,8","4,9","4,10","4,11","4,12"], ["5,0","5,1","5,2","5,3","5,4","5,5","5,6","5,7","5,8","5,9","5,10","5,11","5,12"],["6,0","6,1","6,2","6,3","6,4","6,5","6,6","6,7","6,8","6,9","6,10","6,11","6,12"],  ["7,0","7,1","7,2","7,3","7,4","7,5","7,6","7,7","7,8","7,9","7,10","7,11","7,12"],["8,0","8,1","8,2","8,3","8,4","8,5","8,6","8,7","8,8","8,9","8,10","8,11","8,12"],["9,0","9,1","9,2","9,3","9,4","9,5","9,6","9,7","9,8","9,9","9,10","9,11","9,12"],["10,0","10,1","10,2","10,3","10,4","10,5","10,6","10,7","10,8","10,9","10,10","10,11","10,12"],["11,0","11,1","11,2","11,3","11,4","11,5","11,6","11,7","11,8","11,9","11,10","11,11","11,12"]
while(True):
    minha_posicao = 0
    linha_inicio = 10
    coluna_inicio = 10
    
    tempo = scan_gasoduto()
    print(tempo)
