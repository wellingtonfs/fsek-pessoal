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
gy = GyroSensor(INPUT_1)
gy.mode = 'GYRO-ANG'

#Sensores
m1 = LargeMotor('outD') #Esquerdo
m2 = LargeMotor('outC') #Direito
#m3 = MediumMotor('outB') #Motor mais alto
#m4 = MediumMotor('outA') #Motor mais baixo

#Sensor_Cor = [ColorSensor('in1'), ColorSensor('in2')] #1 = Esquerdo, 2 = Direito
'''
cor = ColorSensor('in1') #2
cor2 = ColorSensor('in2') #4
'''
#us = UltrasonicSensor('in3')
#us2 = UltrasonicSensor('in4')

#Sensor_Cor[0].mode = 'COL-COLOR'
#Sensor_Cor[1].mode = 'COL-COLOR'
#us.mode = 'US-DIST-CM'
#us2.mode = 'US-DIST-CM'

#ir = InfraredSensor('in4') #Era no 3
#ir2 = InfraredSensor('in1')

'''
ir.mode = 'IR-PROX'
ir2.mode = 'IR-PROX'
'''

#Variaveis de uso geral
Estado = 96 #0 = inicio, 1 = ...
Pos_Cores = [[0,10],[0,15],[0,20]] #(x = 10), (y = 15), (z = 20) 
Cor_Anterior = 0
Tempo_Cor = 0
dif_temp = 0

#------FIM DAS VARIÁVEIS

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
    
    #Codigo Lucas
    color_name = ""

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
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(('169.255.168.150', 3564))
                    s.listen()
                    while True:
                        conn, addr = s.accept()
                        with conn:
                            while True:
                                data = conn.recv(1024)

                                if not data:
                                    break

                                Sedex = json.loads(data.decode())
                                self.ir_value = Sedex['IR1']
                                self.ir2_value = Sedex['IR2']

            except Exception as e:
                print(e)
                time.sleep(0.5)
        
Comm = Communication()
Comm.daemon = True
Comm.start()

#------Inicio Funções:

def giraRobo(graus, tempo = 2): #90 > 0: direita else: esquerda
    razaoRobo = 5.25 / 3.0

    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(0.3)

    if graus > 0:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=280,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=280,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=-(razaoRobo*(graus*-1)),speed_sp=280,stop_action="brake")
        m2.run_to_rel_pos(position_sp=(razaoRobo*(graus*-1)),speed_sp=280,stop_action="brake")
    if tempo != 0:
        time.sleep(tempo)

def Emergencia(graus):
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    m1.run_to_rel_pos(position_sp=-400,speed_sp=200,stop_action="brake")
    m2.run_to_rel_pos(position_sp=-400,speed_sp=200,stop_action="brake")
    time.sleep(3)
    giraRobo(graus)
    m1.run_forever(speed_sp=300)
    m2.run_forever(speed_sp=300)

def gyro(an):
    baseAngle = gy.value()

    mdiff.turn_left(SpeedRPM(40), an)
    time.sleep(0.5)

    angle = abs(gy.value() - baseAngle)
    diffAng = angle - an

    if(diffAng < 0):
        mdiff.turn_left(SpeedRPM(40), abs(diffAng))
    else:
        mdiff.turn_right(SpeedRPM(40), abs(diffAng))
    time.sleep(2)

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
        if (us.value() < 400):
            while (us.value() < 100):
                m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    else: 
        while (us.value() > 45):
                m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    time.sleep(2)

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

'''def Para_Motor_Medium(speed):
    while True:
        m3.run_forever(speed_sp=speed)
        m4.run_forever(speed_sp=-speed)

        sumSpeedM3 = 0
        sumSpeedM4 = 0

        for i in range(0, 15):
            if (i < 5):
                continue
            sumSpeedM3 = sumSpeedM3 + m3.speed
            sumSpeedM4 = sumSpeedM4 + m4.speed
        limite = speed * 0.95
        
        sumSpeedM3 = sumSpeedM3 / 10
        sumSpeedM4 = abs(sumSpeedM4 / 10)

        if (sumSpeedM3 < limite) or (sumSpeedM4 < limite):
            m3.stop(stop_action="brake")
            m4.stop(stop_action="brake")
            break

def Mov_Garra_Gasoduto():
    if (us.value() < 120):
        while (us.value() < 90):
            print (ir.value())
            m3.run_to_rel_pos(position_sp=-50,speed_sp=150,stop_action="brake")
            m4.run_to_rel_pos(position_sp=50,speed_sp=150,stop_action="brake")

        while (ir.value() > 127): 
            m1.run_forever(speed_sp=150)
            m2.run_forever(speed_sp=150)
        time.sleep(0.5)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        time.sleep(2)

        #Sobe a garra
        m3.run_to_rel_pos(position_sp=-120,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=120,speed_sp=150,stop_action="brake")
        
        while (ir.value() > 10):
            m1.run_forever(speed_sp=150)
            m2.run_forever(speed_sp=150)
            time.sleep(0.5)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")

        #Desce a garra
        m3.run_to_rel_pos(position_sp=50,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=-50,speed_sp=150,stop_action="brake")

        #Anda para tras     
        while (ir.value() > 127):
            m1.run_forever(speed_sp=-150)
            m2.run_forever(speed_sp=-150)
            time.sleep(0.5)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")

        #Desce a garra
        m3.run_to_rel_pos(position_sp=-120,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=120,speed_sp=150,stop_action="brake")

    #Anda para tras
    while (ir.value() > 18):
        m1.run_forever(speed_sp=-150)
        m2.run_forever(speed_sp=-150)
        time.sleep(0.5)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")

    #Desce a garra
    m3.run_to_rel_pos(position_sp=-120,speed_sp=150,stop_action="brake")
    m4.run_to_rel_pos(position_sp=120,speed_sp=150,stop_action="brake")

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
'''

def Modulo(x):
    if x < 0:
        return x * -1
    return x 

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
                if Modulo(leitura - leitura_anterior) >= variacao:
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
'''
def scan_sup(): #Para entradas do gasoduto
    ti, tf = -1, -1
    m1.run_forever(speed_sp=150)
    m2.run_forever(speed_sp=150)
    if alinhar(2) == 0:
        m1.run_forever(speed_sp=150)
        m2.run_forever(speed_sp=150)
        time.sleep(2)
        giraRobo(-90)
    while True:
        if (us.value() <= 570):
            while (110 < us.value() < 338):
                m1.run_forever(speed_sp=150)
                m2.run_forever(speed_sp=150)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            time.sleep(2)
            ti = time.time()

            while (338 < us.value() < 570):
                m1.run_forever(speed_sp=150)
                m2.run_forever(speed_sp=150)
                time.sleep(0.5)
            tf = time.time()
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            time.sleep(2)

        x = ((((tf-ti)/2)*1000)+1000)

        m1.run_timed(time_sp=x, speed_sp=-150, stop_action="brake")
        m2.run_timed(time_sp=x, speed_sp=-150, stop_action="brake")
        time.sleep(5)

        giraRobo(90)

        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        
        while (ir.value() > 27):
            print ("%d" %ir.value())
            m1.run_forever(speed_sp=150)
            m2.run_forever(speed_sp=150)
            time.sleep(2)

        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        time.sleep(30)'''

def scan_gasoduto():
    tempo_inicio, tempos_pista, anterior_leitura = -1, [], 0
    ti, tf = -1, -1
    tempo_dez, tempo_quinze, tempo_vinte = 0,0,0
    m1.run_forever(speed_sp=150)
    m2.run_forever(speed_sp=150)
    if alinhar(2) == 0:
        m1.run_forever(speed_sp=150)
        m2.run_forever(speed_sp=150)
        time.sleep(2)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        giraRobo(-90)
    while True:
        m1.run_forever(speed_sp=150)
        m2.run_forever(speed_sp=150)
        if us.value() > 36 or us2.value() > 36:
            m1.stop_action("brake")
            m2.stop_action("brake")
            giraRobo(180)
            if len(tempos_pista) > 1:
                tempos_pista.append(time.time())
        elif anterior_leitura == -1:
            tempos_pista.append(time.time()) 
            anterior_leitura = Comm.ir2_value
        elif (Comm.ir2_value - anterior_leitura) > 20: #Descobre um vao
            tempos_pista.append(time.time())
            anterior_leitura = Comm.ir2_value
            if tempo_inicio == 0:
                tempo_inicio = time.time()
        elif (Comm.ir2_value - anterior_leitura) < 20: #Vao fechou
            tempos_pista.append(time.time())
            anterior_leitura = Comm.ir2_value
            if (time.time() - tempo_inicio) > 0:
                print(str(time.time() - tempo_inicio))
                time.sleep(15)

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
                if 40 < us2.value() < 400:
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
                if 40 < us.value() < 400:
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
        elif 40 < us.value() < 400:
            Emergencia(90)
        elif 40 < us2.value() < 400:
            Emergencia(-90)

        m1.run_forever(speed_sp=300)
        m2.run_forever(speed_sp=300)

while True:
    if Estado == 0:
        Encontrar_Pos() #Se achar na parte superior da pista
        Estado = 1

    elif Estado == 1:
        a = blakeLine() #Saber as posições das cores
        print(a)
        time.sleep(10)
        #andar na linha, descobrindo as cores

    elif Estado == 2:
        while True:
            if LeituraIR(2) < 40:
                AchouCano()
        #descobrir os espaços na tubulação
    elif Estado == 3:
        m1.run_forever(speed_sp=150)
        m2.run_forever(speed_sp=150)

        if alinhar(2) == 0:
            m1.run_to_rel_pos(position_sp=700,speed_sp=150,stop_action="brake")
            m2.run_to_rel_pos(position_sp=700,speed_sp=150,stop_action="brake")
            time.sleep(2)
            giraRobo(-90) 
        #voltar para pegar os tubos
    elif Estado == 4:
        m1.run_forever(speed_sp=300)
        m2.run_forever(speed_sp=-300)

        while True:
            if 45 < Comm.ir_value < 60:
                m1.run_forever(speed_sp=100)
                m2.run_forever(speed_sp=100)
            elif Comm.ir_value <= 45:
                #AchouCano()
                time.sleep(10)
    elif Estado == 5:
        giraRobo(80)
        m1.run_forever(speed_sp=100)
        m2.run_forever(speed_sp=100)
        while True:
            if 46 <= Comm.ir_value <= 90:
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                giraRobo(-143)
                m1.run_forever(speed_sp=100)
                m2.run_forever(speed_sp=100)
                time.sleep(10)
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                time.sleep(10)
    elif Estado == 42:
        scan_gasoduto()
    elif Estado == 69:
        scan_sup()
    elif Estado == 96:
        gyro()
'''

cont = 0
    tempos_media, Leituras_ir = [], []
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
        giraRobo(-40)

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

'''