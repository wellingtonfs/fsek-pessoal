#!/usr/bin/env python3
#coding: utf-8
import socket, json
from ev3dev.ev3 import *
from threading import *

import time
import math

from ev3dev2.motor import OUTPUT_C, OUTPUT_D, MoveTank

sc = ColorSensor('in1')
sc2 = ColorSensor('in2')

sc.mode = 'COL-COLOR'
sc2.mode = 'COL-COLOR'

tank = MoveTank(OUTPUT_C, OUTPUT_D)

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
m3 = MediumMotor('outB') #Motor mais alto
m4 = MediumMotor('outA') #Motor mais baixo

gy = GyroSensor('in3')
gy.mode = 'GYRO-ANG'

ub = UltrasonicSensor('in4')
ub.mode = 'US-DIST-CM'

ubL = 0

def alinhar(c): #Essa função alinha o lego a uma cor especifica c.
    if sc.value() == c and sc2.value() ==  c:
        if ruido(c):
            return True

    while True:
        print(sc.value(), sc2.value())
        if sc.value() == c:
            tank.stop()

            while sc.value() == c:
                tank.on(-10, -10)

            tank.stop()
            tank.on(10, 0)

            while sc2.value() != c:
                tank.on(0, 10)
            
            while sc2.value() == c:
                tank.on(0, -10)
                
            break

        if sc2.value() == c:
            tank.stop()

            while sc2.value() == c:
                tank.on(-10, -10)

            tank.stop()
            tank.on(0, 10)

            while sc.value() != c:
                tank.on(10, 0)

            while sc.value() == c:
                tank.on(-10, 0)

            break

    tank.stop()

    return False

def ruido(color):
    count = 0
    for i in range(0,5):
        print("ruido:", sc.value(), sc2.value())
        tank.on_for_degrees(10, 10, 10)
        if sc.value() == color or sc2.value() == color:
            count += 1

        tank.on_for_degrees(10, 10, -10)
        if sc.value() == color or sc2.value() == color:
            count += 1

    tank.on_for_degrees(10, 10, -10)

    if count > 8:
        return True

    return False

def walkUntilColor(color, speed = 10, limit = 0):
    tank.on(speed, speed)
    count = 0

    while True:
        while sc.value() != color and sc2.value() != color:
            count += 1
            if(limit != 0 and count > limit):
                return False

        # se nã0 passar no ruido continua andando
        if ruido(color):
            break
        else:
            tank.on(speed, speed)

    tank.stop()

    print("Chegou na cor:", color)
    return True

def rotateCm(cm, speed = 15):
    degrees = cm * 360 / 17.6

    positionBase = m1.position

    if(cm < 0):
        speed = -speed

    tank.on(speed, speed)
    
    while abs(m1.position - positionBase) <= abs(degrees):
        pass
    tank.stop()

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
        self.ut_value = 0
        self.ir_value = 0
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
                                self.ut_value = Sedex['ut']
                                self.ir_value = Sedex['ir']
                                self.uf_value = Sedex['uf']
            except Exception as e:
                print(e)
                time.sleep(0.5)

Comm = Communication()
Comm.daemon = True
Comm.start()

def Testar_Dist():
    lego.parar()

    def g(valor, a):
        if a:
            m1.run_to_rel_pos(position_sp=-valor, speed_sp=100, stop_action="brake")
            m2.run_to_rel_pos(position_sp=valor, speed_sp=100, stop_action="brake")
        else:
            m1.run_to_rel_pos(position_sp=valor, speed_sp=100, stop_action="brake")
            m2.run_to_rel_pos(position_sp=-valor, speed_sp=100, stop_action="brake")

    valores = []
    somar = 0
    for i in [True, False, False, True]:
        u = ub.value()
        valores.append(u)
        somar += u
        g(30, i)
        time.sleep(0.5)

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

class andar(Thread):
    def __init__(self):
        self.andando = False
        self.parando = False
        self.vel = 200
        self.ang = 0
        self.ang2 = 0.2
        self.parado = False
        Thread.__init__(self)

    def run(self):
        global ubL

        while True:
            if self.andando:
                speed1, speed2 = self.vel, self.vel

                while self.parando == False:
                    if self.ang == 0:
                        m1.run_forever(speed_sp=self.vel)
                        m2.run_forever(speed_sp=self.vel)
                    else:
                        leitura = ubL

                        if leitura > 2548:
                            leitura = self.ang

                        #tratamento da leitura
                        #v = abs(gy.value() - self.ang2)
                        #if v != 0:
                        #    leitura = ubL * math.cos((1*(v/57.2958)))

                        s = ""
                        leitura = abs(leitura)
                        if leitura < self.ang:
                            variacao = 10*(self.ang - leitura)
                            s += "1: " + str(variacao) + ", vels: "
                            if variacao > 60:
                                variacao = 60
                            if self.vel > 0:
                                speed2 = self.vel + (variacao/3)
                            else:
                                speed2 = self.vel - (variacao/3)
                            speed1 = self.vel
                            s += str(speed1) + ", " + str(speed2) + ".  ang: " + str(self.ang) + ", leitura: " + str(leitura)
                            print(s)
                        elif leitura > self.ang:
                            variacao = 10*(leitura - self.ang) 
                            s += "2: " + str(variacao) + ", vels: "
                            if variacao > 60:
                                variacao = 60
                            if self.vel > 0:
                                speed1 = self.vel + (variacao/3)
                            else:
                                speed1 = self.vel - (variacao/3)
                            speed2 = self.vel
                            s += str(speed1) + ", " + str(speed2) + ".  ang: " + str(self.ang) + ", leitura: " + str(leitura)
                            print(s)
                        else:
                            speed1, speed2 = self.vel, self.vel
                            print("caiu no else")

                        m1.run_forever(speed_sp=speed2)
                        m2.run_forever(speed_sp=speed1)

                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")

                self.andando = False
                self.parando = False
                self.ang = 0
                self.ang2 = 0
                self.parado = False

    def andar(self, speed = -150, dist = 0, angulo = 0.2):
        while self.parado:
            pass
        self.andando = True
        self.parando = False
        self.vel = speed
        self.ang = dist
        self.ang2 = angulo

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

def Mov_Garra_Analog(Sentido, Pos): 
    if Sentido:
        m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
        time.sleep(1)
    else:
        m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
        time.sleep(1)

def Cano_Suporte(pos):
    Mov_Garra_Analog(1, 100)
    lego.andar_tempo(speed=100, tempo=4)
    Mov_Garra_Analog(0, 180)

    time.sleep(2)

    m1.run_to_rel_pos(position_sp=-pos,speed_sp=250,stop_action="brake")
    m2.run_to_rel_pos(position_sp=-pos,speed_sp=250,stop_action="brake")
    time.sleep(2)

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
    Cano_Suporte(200)
    rotateTo(-90)
    lego.andar_tempo(speed=150, tempo=tempo)


controleEstado = False
def c_tubo(tam_tubo):
    global ubL, controleEstado
    Estado = 2
    var_est = False
    while True:
        if Estado == 0: #chegar no gasoduto pela primeira vez
            print("Esperando comunicacao..")
            while Comm.ut_value == 0:
                pass

            lego.andar()

            print("indo ate o gasoduto")
            while Comm.ut_value > 150:
                print(Comm.ut_value)

            lego.parar()
            print("saiu do while de ir ate o gasoduto")
            rotateTo(90)

            if controleEstado:
                walkUntilColor(0)
                alinhar(0)
                controleEstado = False

            Estado = 1
            
        elif Estado == 1: #andar paralelo ao gasoduto
            lego.parar()
            tank.stop()

            ubL = ub.value()
            lego.andar(dist=150, angulo=gy.value())

            time_vao = 0
            time_entrada = 0

            print("Entrou while procurar cano")
            while Comm.ut_value > 110: #verificar queda dps
                try:
                    ubL = ub.value()
                except Exception as e:
                    print(e)

                if Comm.uc_value > 200 and time_entrada == 0:
                    print("Inicio tubo")
                    time_entrada = time.time()
                elif Comm.uc_value < 200 and time_entrada != 0:
                    tempo_dif = (time.time() - time_entrada)
                    if tempo_dif > 1.1:
                        if tam_tubo == 10 or (tam_tubo == 15 and tempo_dif > 2) or (tam_tubo == 20 and tempo_dif > 2.5):
                            print("colocou tubo")
                            #Entregar_Tubo(tempo=tempo_dif, tam=tam_tubo)
                            #return True
                        else:
                            print("Nao cabe", tempo_dif)
                    else:
                        print("vao falso", tempo_dif)
                    time_entrada = 0

                if ubL > 200 and time_vao == 0:
                    time_vao = time.time()
                elif time_vao != 0 and (time.time() - time_vao) > 0.5:
                    if ubL > 200 and var_est:
                        Estado = 3
                        print("detectou vao")
                        break
                    else:
                        time_vao = 0

                if Comm.ir_value > 21:
                    pass
                    #lego.parar()
                    #Estado = 4
                    #print("detectou queda")
                    #break

            if Estado == 1:
                Estado = 2

            print("Saiu while procurar cano")

        elif Estado == 2: #dobrar a direita
            
            print("Entrou em dobrar 1")
            lego.andar_tempo(speed=-150, tempo=3)

            lego.parar()
            tank.stop()

            rotateCm(10)
            rotateTo(-90)

            walkUntilColor(3)
            alinhar(3)

            rotateCm(-20)
            rotateTo(90)

            rotateCm(-45)
            rotateTo(-90)

            Estado = 0
            var_est = True

        elif Estado == 3: #dobrar a esquerda
            lego.parar()
            tank.stop()
            print("Entrou em dobrar 2")
            
            rotateCm(-30)
            rotateTo(-90)

            Estado = 0 
            print("Saiu andar 2")

        elif Estado == 4: #final do gasoduto e fim da funcao
            print("Fim da funcao")
            return False

print(c_tubo(10))