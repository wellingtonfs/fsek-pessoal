#!/usr/bin/env python3
from ev3dev.ev3 import *
from threading import *
import time
import math

#------VARIÁVEIS DO PROGRAMA

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
cor = ColorSensor('in2')
cor2 = ColorSensor('in4')
ir = InfraredSensor('in3')
#us2 = UltrasonicSensor('in3')

cor.mode = 'COL-COLOR'
cor2.mode = 'COL-COLOR'
ir.mode = 'IR-PROX'
#us2.mode = 'US-DIST-CM'

#alinhado = False
Ativar_Emergencia = True
Estado = 0 #0 = inicio, 1 = ...
Cor_Anterior = 0
Tempo_Cor = 0
dif_temp = 0

#------FIM DAS VARIÁVEIS

def giraRobo(graus, sentido): #Essa função gira o robo para algum lado
    razaoRobo = (2 * math.pi * 5.5) / (2 * math.pi * 2.71)
    if sentido:
        m2.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
        m1.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=180,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=180,stop_action="brake")
    time.sleep(2)

class vals(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global Estado, Cor_Anterior, dif_temp
        while True:
            print(ir.value())
            if 46 <= ir.value() <= 60:
                if Estado == 1:
                    Estado = -1
                    m1.stop(stop_action="brake")
                    m2.stop(stop_action="brake")
                    giraRobo(180, True)
                    Cor_Anterior = cor.value()
                    dif_temp = 0
                    Estado = 1
                else:
                    if Estado == 0:
                        Emergencia()
            #print(str(ir.value()))
            time.sleep(1)

oi = vals()
oi.start()

def Emergencia():
    global Ativar_Emergencia
    if Ativar_Emergencia:
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        m1.run_to_rel_pos(position_sp=-400,speed_sp=200,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-400,speed_sp=200,stop_action="brake")
        time.sleep(3)
        giraRobo(120, True)
        m1.run_forever(speed_sp=300)
        m2.run_forever(speed_sp=300)

def Intervalos(Intervalo): #Saber se o intervalo ta crescendo, decrescendo ou os dois
    c, d = 0, 0 #crescer / decrescer
    for i in range(1, len(Intervalo), 1):
        if (Intervalo[i] - Intervalo[i-1]) > 0:
            c += 1
        elif (Intervalo[i] - Intervalo[i-1]) < 0:
            d += 1

    c = (c / len(Intervalo)) * 100
    d = (d / len(Intervalo)) * 100

    if 45 <= c <= 55 and 45 <= d <= 55:
        return "Al" #alinhado
    elif c > 80:
        return "Dr" #dobrar para direita
    elif d > 80:
        return "Eq" #dobrar para esquerda
    else:
        return False

def AchouCano():
    cont = 0
    tempos_media, Leituras_ir = [], []
    print("Entrou F")
    while True:
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")

        leitura = ir.value()
        if leitura > 99:
            continue
        while leitura <= 45:
            leitura = ir.value()
            if leitura > 99:
                continue
            m1.run_forever(speed_sp=-70)
            m2.run_forever(speed_sp=70)

        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")

        tempo_giro = 0
        Leituras_ir, tempo_lt = [], time.time()

        while True:
            leitura = ir.value()
            if leitura > 99:
                continue
            m1.run_forever(speed_sp=70)
            m2.run_forever(speed_sp=-70)

            if (time.time() - tempo_lt) > 0.08:
                Leituras_ir.append(leitura)
                tempo_lt = time.time()

            if leitura <= 45 and tempo_giro == 0:
                tempo_giro = time.time()
            else:
                if leitura > 45 and tempo_giro != 0:
                    break

        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        if tempo_giro != -1:
            tempos_media.append(time.time() - tempo_giro)
            cont += 1
            if cont > 2:
                break
        giraRobo(40, True)

    media, cc = 0, 0
    for i in tempos_media:
        media += i
        cc += 1

    media /= cc
    print(str(int(media*1000)))
    Qual_direcao = Intervalos(Leituras_ir)
    if Qual_direcao == "al":
        print("Alinhado")
        time.sleep(3)
        #voltar ao meio do tubo
    elif Qual_direcao == "Dr":
        m1.run_timed(time_sp=int(media*1000), speed_sp=70)
        m2.run_timed(time_sp=int(media*1000), speed_sp=-70)
    else:
        media *= 2
        m1.run_timed(time_sp=int(media*1000), speed_sp=-70)
        m2.run_timed(time_sp=int(media*1000), speed_sp=70)
    time.sleep((int(media*1000) + 1))
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")

def alinhar(c): #Essa função alinha o lego a uma cor especifica c.
    if cor.value() == c and cor2.value() == c:
        return 0
    while True:
        if cor.value() == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while cor.value() == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            #m1.run_forever(speed_sp=-150)
            m2.run_forever(speed_sp=100)
            while cor2.value() != c:
                if cor2.value() == 0:
                    return 1
                if cor.value() != c:
                    m1.run_forever(speed_sp=70)
                else:
                    m1.stop(stop_action="brake")
            return 0

        if cor2.value() == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while cor2.value() == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            m1.run_forever(speed_sp=100)
            #m2.run_forever(speed_sp=-150)
            while cor.value() != c:
                if cor.value() == 0:
                    return 1
                if cor2.value() != c:
                    m2.run_forever(speed_sp=70)
                else:
                    m2.stop(stop_action="brake")
            return 0

m1.run_forever(speed_sp=300)
m2.run_forever(speed_sp=300)
#tdetempo = time.time()

while True:
    if Estado == 0:
        if cor.value() == 1 or cor2.value() == 1: #Preto
            if alinhar(1) == 1:
                Emergencia()
            else:
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                Estado = 5

    elif Estado == 1:
        pass
        #andar na linha, descobrindo as cores
    elif Estado == 2:
        pass
        #descobrir os espaços na tubulação
    elif Estado == 3:
        pass
        #voltar para pegar os tubos
    elif Estado == 4:
        m1.run_forever(speed_sp=300)
        m2.run_forever(speed_sp=-300)

        while True:
            if 45 < ir.value() < 60:
                m1.run_forever(speed_sp=100)
                m2.run_forever(speed_sp=100)
            elif ir.value() <= 45:
                AchouCano()
                time.sleep(10)
    elif Estado == 5:
        giraRobo(80, False)
        m1.run_forever(speed_sp=100)
        m2.run_forever(speed_sp=100)
        while True:
            if 46 <= ir.value() <= 90:
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                giraRobo(143, True)
                m1.run_forever(speed_sp=100)
                m2.run_forever(speed_sp=100)
                time.sleep(10)
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                time.sleep(10)