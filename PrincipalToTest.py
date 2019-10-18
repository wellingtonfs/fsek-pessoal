#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *

from ev3dev2.motor import OUTPUT_C, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import GyroSensor

import time, socket
import math, json
import colorsys

#------VARIÁVEIS DO PROGRAMA

mdiff = MoveDifferential(OUTPUT_D, OUTPUT_C, EV3EducationSetTire, 105)
#Motores
m1 = LargeMotor('outD') #Esquerdo
m2 = LargeMotor('outC') #Direito
m3 = MediumMotor('outB') #Motor mais alto
m4 = MediumMotor('outA') #Motor mais baixo

#Sensores

Sensor_Cor = [ColorSensor('in1'), ColorSensor('in2')] #1 = Esquerdo, 2 = Direito
Sensor_Cor[0].mode = 'COL-COLOR'
Sensor_Cor[1].mode = 'COL-COLOR'

Sensor_Ultrassonico = [UltrassonicSensor('in3'), UltrassonicSensor('in4')] #1 = Esquerdo, 2 = Direito
Sensor_Ultrassonico[0].mode = 'US-DIST-CM'
Sensor_Ultrassonico[1].mode = 'US-DIST-CM'

#Variaveis globais
Estado = -1 #0 = inicio, 1 = ...
Cor_Anterior = 0
matriz_gasoduto = []

for i in range(2):
    linha = []
    for j in range(16):
        linha.append(0)
    matriz_gasoduto.append(linha)

def convertHSV(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return (h, s, v)

def convertRGB(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (r, g, b)

def Verifica_Cor(x,y,z):
    #(x, y, z) = cor3.value(0), cor3.value(1), cor3.value(2)
    x = x/1023
    y = y/1023
    z = z/1023
    
    (h, s, v) = convertHSV(x, y, z)
    
    s = 0.8
    v = 1
    (r, g, b) = convertRGB(h, s, v)
    
    r = r * 255
    g = g * 255
    b = b * 255

    colors = {
        "1": "#000000", #Black
        "5": "#FF0000", #Red
        "4": "#FFFF00", #Yellow
        "3": "#00FF00", #Green
        "2": "#0000FF", #Blue
        "6": "#FFFFFF" #White
    }

    def rgbFromStr(s):
            r, g, b = int(s[1:3],16), int(s[3:5], 16),int(s[5:7], 16)  
            return r, g, b  

    def findNearestColorName(color, Map):  
        (R,G,B) = color
        mindiff = None
        for d in Map:  
            r, g, b = rgbFromStr(Map[d])  
            diff = abs(R-r) * 256 + abs(G-g) * 256 + abs(B-b) * 256   
            if mindiff is None or diff < mindiff:  
                mindiff = diff  
                mincolorname = d  
        return mincolorname    

    return findNearestColorName((r, g, b), colors)
    
class Communication(Thread):
    def __init__(self):
        self.ir_value = 0
        self.ir2_value = 0
        self.gy_value = 0
        self.us3_value = 0
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(('169.255.168.150', 3563))
                    s.listen()
                    while True:
                        conn, addr = s.accept()
                        with conn:
                            #print('Connected by', addr)
                            while True:
                                data = conn.recv(1024)

                                if not data:
                                    break

                                Sedex = json.loads(data.decode())
                                self.ir_value = Sedex['IR1']
                                self.ir2_value = Sedex['IR2']
                                self.gy_value = Sedex['GY']
                                self.us3_value = Sedex['US']

            except Exception as e:
                print(e)
                time.sleep(0.5)
        
Comm = Communication()
Comm.daemon = True
Comm.start()

#------Inicio Funções:

def Emergencia(graus):
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    m1.run_to_rel_pos(position_sp=-400,speed_sp=200,stop_action="brake")
    m2.run_to_rel_pos(position_sp=-400,speed_sp=200,stop_action="brake")
    time.sleep(3)
    giraRobo(graus)
    m1.run_forever(speed_sp=300)
    m2.run_forever(speed_sp=300)

def giraRobo(graus, speed = 130):
    angleBase = Comm.gy_value
    if graus > 0:
        left_speed = speed
        right_speed = -speed
    else: 
        left_speed = speed
        right_speed = -speed

    graus = abs(graus)

    m1.run_forever(left_speed)
    m2.run_forever(right_speed)
    while abs(angleBase - Comm.gy_value) < graus:
        pass
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    

def blakeLine(): #Walk the black line to learning colors.
    global Estado, Cor_Anterior
    x, y, z, ini = -1, -1, -1, False #variaveis para salvar as posições das cores
    variavel_tempo = time.time()
    m1.run_to_rel_pos(position_sp=400, speed_sp=100) #andar até o robo entrar na cor totalmente
    m2.run_to_rel_pos(position_sp=400, speed_sp=100)
    time.sleep(3)
    giraRobo(-90) #Girar para dobrar paralelo a linha preta
    Leitura = [Sensor_Cor[0].value(), Sensor_Cor[1].value()]
    Cor_Anterior = Leitura[0]
    while Leitura[0] != Leitura[1]: #contar o tempo para nao andar infinitamente
        m1.run_to_rel_pos(position_sp=-360, speed_sp=70)
        m2.run_to_rel_pos(position_sp=-360, speed_sp=70)
        Leitura[0] = Sensor_Cor[0].value()
        Leitura[1] = Sensor_Cor[1].value()
        Cor_Anterior = Leitura[0]
        if (time.time() - variavel_tempo) > 3:
            pass

    variavel_tempo = time.time()
    while True:
        m1.run_forever(speed_sp=300)
        m2.run_forever(speed_sp=300)
        if Sensor_Cor[0].value() != Cor_Anterior:
            if alinhar(Sensor_Cor[0].value()) != 0:
                Emergencia(120)
                return 0
            Cor_Anterior = Sensor_Cor[0].value()
            if ini:
                if x != -1 and y == -1:
                    y = Cor_Anterior
        elif Sensor_Cor[1].value() != Cor_Anterior:
            if alinhar(Sensor_Cor[1].value()) != 0:
                Emergencia(120)
            Cor_Anterior = Sensor_Cor[1].value()
            if ini:
                if x != -1 and y == -1:
                    y = Cor_Anterior

        if (time.time() - variavel_tempo) > 0.5:
            print("ir: %d" %Comm.ir_value)
            variavel_tempo = time.time()
        if 30 <= Comm.ir_value <= 99:
            giraRobo(-180)
            if x == -1:
                x = Cor_Anterior
                print("color x: %d" %x)
            elif y != -1:
                z = Cor_Anterior
                print("color z: %d" %z)
                break
            ini = True

    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    return [x,y,z]

def Verificar_Ruido(Sensor): #fazer a função de ruido dos sensores de cor
    if Sensor == 1:
        return Sensor_Cor[0].value()
    else:
        return Sensor_Cor[1].value()

def Mov_Garra_Sensor(Sentido, Pos): #0 = descer; 1 = subir;
    if Sentido: 
        if (Comm.us3_value < 400):
            while (Comm.us3_value < 100):
                m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    else: 
        while (Comm.us3_value > 45):
                m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    time.sleep(2)

def Mov_Garra_Analog(Sentido, Pos):
    if Sentido:
        m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
    else:
        m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")

def LeituraIR(QIr): #fazer ele "vibrar" para não ler sempre a mesma coisa
    global Comm
    if QIr == 1:
        leitura = Comm.ir_value
        while leitura > 99:
            leitura = Comm.ir_value
        return leitura
    else:
        leitura = Comm.ir2_value
        while leitura > 99:
            leitura = Comm.ir2_value
        return leitura

def AchouCano():
    Estado_Local = 0
    Medidas = [0, 0, False] #inicio cano, fim cano, caso tenho mudado o fim do cano
    while True:
        if Estado_Local == 0:
            while LeituraIR(2) <= 50:
                m1.run_forever(speed_sp=-70)
                m2.run_forever(speed_sp=70)
            
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")

            leitura = LeituraIR(2)
            while leitura > 50:
                m1.run_forever(speed_sp=70)
                m2.run_forever(speed_sp=-70)
            
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            Medidas[0] = LeituraIR(2)
            Estado_Local = 1

        elif Estado_Local == 1:
            variacao, leitura_anterior = 3, 0 #caso tenha alguma descida ou subida na leitura do sensor
            tempo_g = [time.time(), False] #esse false é para saber ja ja pegou o tempo
            leitura = LeituraIR(2)
            leitura_anterior = leitura
            while leitura <= 50:
                m1.run_forever(speed_sp=70)
                m2.run_forever(speed_sp=-70)
                leitura = LeituraIR(2)
                if abs(leitura - leitura_anterior) >= variacao:
                    if (leitura - leitura_anterior) < 0: #caso ele ache uma variação grande na medição, ele zera as variaveis
                        Medidas[0] = leitura
                        tempo_g[0] = time.time()
                    else:
                        Medidas[1] = leitura
                        tempo_g[0] = time.time() - tempo_g[0]
                        tempo_g[1] = True

            if not tempo_g[1]:
                tempo_g[0] = time.time() - tempo_g[0]

            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            print(str(tempo_g[0]))
            time.sleep(10)

def scan_gasoduto():
    pos_eu = -1
    tempo_pos = 0
    while True:
        if (Sensor_Ultrassonico[0].value() > 36 or Sensor_Ultrassonico[1].value() > 36):
            m1.stop_action("brake")
            m2.stop_action("brake")
            
            m1.run_timed(time_sp=70, speed_sp=-180, stop_action="brake")
            m2.run_timed(time_sp=70, speed_sp=-180, stop_action="brake")
            time.sleep(2)
            
            m1.stop_action("brake")
            m2.stop_action("brake")

            giraRobo(180)
        
        else:
            if (time.time() - tempo_pos) > 3 and pos_eu < 16:
                m1.run_to_rel_pos(position_sp=153,speed_sp=150,stop_action="brake")
                m2.run_to_rel_pos(position_sp=153,speed_sp=150,stop_action="brake")
                pos_eu += 1
                tempo_pos = time.time()
            else:
                if pos_eu >= 16:
                    pass
                    #fim

            if Comm.ir2_value > 50:
                matriz_gasoduto[1][pos_eu] = 1
            if Comm.ir_value > 50:
                matriz_gasoduto[0][pos_eu] = 2


def alinhar(c): #Essa função alinha o lego a uma cor especifica c.
    if Sensor_Cor[0].value() == c and Sensor_Cor[1].value() == c:
        return 0
    while True:
        if Sensor_Cor[0].value() == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while Sensor_Cor[0].value() == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            #m1.run_forever(speed_sp=-150)
            m2.run_forever(speed_sp=100)
            while Sensor_Cor[1].value() != c:
                if Sensor_Cor[1].value() == 0:
                    return 1
                if Sensor_Cor[0].value() != c:
                    m2.stop(stop_action="brake")
                    m1.run_forever(speed_sp=70)
                else:
                    m1.stop(stop_action="brake")
                    m2.run_forever(speed_sp=100)
                if 40 < Sensor_Ultrassonico[1].value() < 400:
                    return 2
            break

        if Sensor_Cor[1].value() == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while Sensor_Cor[1].value() == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            m1.run_forever(speed_sp=100)
            #m2.run_forever(speed_sp=-150)
            while Sensor_Cor[0].value() != c:
                if Sensor_Cor[0].value() == 0:
                    return 1
                if Sensor_Cor[1].value() != c:
                    m1.stop(stop_action="brake")
                    m2.run_forever(speed_sp=70)
                else:
                    m1.run_forever(speed_sp=100)
                    m2.stop(stop_action="brake")
                if 40 < Sensor_Ultrassonico[0].value() < 400:
                    return 1
            break

    m1.run_forever(speed_sp=250)
    m2.run_forever(speed_sp=250)
    time.sleep(1)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    return 0

def Encontrar_Pos():
    while True:#Comm.ir_value
        if Sensor_Cor[0].value() == 1 or Sensor_Cor[1].value() == 1: #Se achar Preto
            Al = alinhar(1)
            if Al == 1:
                Emergencia(80)
            elif Al == 2:
                Emergencia(-80)
            else:
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                return 0
        elif Sensor_Cor[0].value() == 3 or Sensor_Cor[1].value() == 3: #Se achar Verde
            Emergencia(180)
        elif 40 < Sensor_Ultrassonico[0].value() < 400:
            Emergencia(90)
        elif 40 < Sensor_Ultrassonico[1].value() < 400:
            Emergencia(-90)

        m1.run_forever(speed_sp=300)
        m2.run_forever(speed_sp=300)

while True:
    if Estado == 0: #Se achar na pista
        Encontrar_Pos()
        Estado = 1
        pass
    elif Estado == 1: #Achar cor tubo pequeno
        blakeLine()
        Estado = 2
        pass
    elif Estado == 2: #Procurar e pegar tubo
        Estado = 3
        pass
    elif Estado == 3: #Acha extremidade correta
        Estado = 4
        pass
    elif Estado == 4: #Procura o vão de 10cm já guardando a posição dos demais
        Estado = 5
        pass
    elif Estado == 5: #Se alinha com o vão para largar o tubo
        Estado = 6
        pass
    elif Estado == 6: #Larga o tubo no lugar certo
        Estado = 7
        pass
    elif Estado == 7: #Volta para pegar o tubo que quisermos
        Estado = 8
        pass
    elif Estado == 8: #Volta ao gasoduto para vão correto
        pass