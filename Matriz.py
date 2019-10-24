#!/usr/bin/env python3
#coding: utf-8
import socket, json
from ev3dev.ev3 import *
from threading import *

import time
import math

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
m3 = MediumMotor('outB') #Motor mais alto
m4 = MediumMotor('outA') #Motor mais baixo

gy = GyroSensor('in3')
gy.mode = 'GYRO-ANG'

ir = InfraredSensor('in4')
ir.mode = 'IR-PROX'

def rotateTo(ang):
    atual = gy.value()
    if ang > 0:
        ang -= 3
        while abs(gy.value() - atual) < abs(ang):
            m1.run_forever(speed_sp=-100)
            m2.run_forever(speed_sp=100)
    else:
        ang += 3
        while abs(gy.value() - atual) < abs(ang):
            m1.run_forever(speed_sp=100)
            m2.run_forever(speed_sp=-100)
    
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")

class Communication(Thread):
    def __init__(self):
        self.uc_value = 0
        self.ub_value = 0
        self.ut_value = 0
        self.uf_value = 0
        Thread.__init__(self)

    def run(self):
        while True:
            try:
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
                                    for i in range(len(st)):
                                        if st[i] == '}':
                                            Sedex = json.loads(st[0:i+1])
                                            break
                                            
                                self.uc_value = Sedex['uc']
                                self.ub_value = Sedex['ub']
                                self.ut_value = Sedex['ut']
                                self.uf_value = Sedex['uf']
            except Exception as e:
                print(e)
                time.sleep(0.5)

Comm = Communication()
Comm.daemon = True
Comm.start()

class andar(Thread):
    def __init__(self):
        self.andando = False
        self.parando = False
        self.vel = 200
        self.ang = 0.2
        self.parado = False
        Thread.__init__(self)

    def run(self):
        while True:
            if self.andando:
                speed1, speed2 = self.vel, self.vel

                while self.parando == False:
                    if self.ang == 0:
                        m1.run_forever(speed_sp=self.vel)
                        m2.run_forever(speed_sp=self.vel)
                    else:
                        if Comm.ub_value < self.ang:
                            variacao = (self.ang - Comm.ub_value)
                            if variacao > 200:
                                variacao = 200
                            if self.vel > 0:
                                speed2 = self.vel + variacao
                            else:
                                speed2 = self.vel - variacao
                        elif Comm.ub_value > self.ang:
                            variacao = (Comm.ub_value - self.ang) 
                            if variacao > 200:
                                variacao = 200
                            if self.vel > 0:
                                speed1 = self.vel + variacao 
                            else:
                                speed1 = self.vel - variacao
                        else:
                            speed1, speed2 = self.vel, self.vel

                        m1.run_forever(speed_sp=(speed2))
                        m2.run_forever(speed_sp=(speed1))

                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")

                self.andando = False
                self.parando = False
                self.ang = 0
                self.parado = False

    def andar(self, speed = -150, dist = 0):
        while self.parado:
            pass
        self.andando = True
        self.parando = False
        self.vel = speed
        self.ang = dist

    def parar(self):
        if self.andando:
            self.parando = True
            self.parado = True

    def andar_tempo(self, speed = 200, dist = 0, tempo = 0):
        self.parar()
        while self.parado:
            pass
        t = time.time()
        while (time.time() - t) <= tempo:
            self.andar(speed=speed, dist=dist)
        self.parar()

lego = andar()
lego.daemon = True
lego.start()

def Entregar_Tubo(tempo = 0, tam=0):
    lego.parar()
    if tam == 10:
        lego.andar_tempo(speed=150, tempo=(tempo - 1))
    elif tam == 15:
        lego.andar_tempo(speed=150, tempo=(tempo - 1.5))
    else:
        lego.andar_tempo(speed=150, tempo=(tempo - 2))
    rotateTo(90)
    print("colocando o tubo")
    #Cano_Suporte(200)
    rotateTo(-90)
    lego.andar_tempo(speed=150, tempo=tempo)

def c_tubo(tam_tubo):
    Estado = 0
    while True:
        if Estado == 0: #chegar no gasoduto pela primeira vez
            print("Esperando comunicacao..")
            while Comm.ut_value == 0:
                pass

            lego.andar()

            print("indo ate o gasoduto")
            while Comm.ut_value > 100:
                print(Comm.ut_value)

            lego.parar()
            print("saiu do while de ir ate o gasoduto")
            rotateTo(90)

            Estado = 1
            
        elif Estado == 1: #andar paralelo ao gasoduto
            lego.andar(dist=90)

            time_vao = 0

            print("Entrou while procurar cano")
            while Comm.ut_value > 90: #verificar queda dps
                if Comm.uc_value > 200 and time_vao == 0:
                    print("Inicio tubo")
                    time_vao = time.time()
                elif Comm.uc_value < 200 and time_vao != 0:
                    tempo_dif = (time.time() - time_vao)
                    if tempo_dif > 1.1:
                        if tam_tubo == 10 or (tam_tubo == 15 and tempo_dif > 2) or (tam_tubo == 20 and tempo_dif > 2.5):
                            Entregar_Tubo(tempo=tempo_dif, tam=tam_tubo)
                            return True
                        else:
                            print("Nao cabe", tempo_dif)
                    else:
                        print("vao falso", tempo_dif)
                    time_vao = 0

                if ir.value() > 30:
                    lego.parar()
                    Estado = 3
                    break

            print("Saiu while procurar cano")
            Estado = 2

        elif Estado == 2: #dobrar em algum angulo
            print("Entrou em dobrar")
            lego.parar()
            rotateTo(90)
            Estado = 1

        elif Estado == 3: #final do gasoduto e fim da funcao
            print("Fim da funcao")

print(c_tubo(10))