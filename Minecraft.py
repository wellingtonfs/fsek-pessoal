#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import time, socket
import math
import colorsys

m1 = LargeMotor('outD') #Esquerdo
m2 = LargeMotor('outC') #Direito

Sensor_Ultrassonico = [UltrassonicSensor('in3'), UltrassonicSensor('in4')] #1 = Esquerdo, 2 = Direito
Sensor_Ultrassonico[0].mode = 'US-DIST-CM'
Sensor_Ultrassonico[1].mode = 'US-DIST-CM'

Sensor_Cor = [ColorSensor('in1'), ColorSensor('in2')] #1 = Esquerdo, 2 = Direito

Sensor_Cor[0].mode = 'COL-COLOR'
Sensor_Cor[1].mode = 'COL-COLOR'

ir = InfraredSensor('in2')
ir.mode = 'IR-PROX'
# def VerificacaoCor():
#     def convertHSV(r, g, b):
#         h, s, v = colorsys.rgb_to_hsv(r, g, b)
#         return (h, s, v)

#     def convertRGB(h, s, v):
#         r, g, b = colorsys.hsv_to_rgb(h, s, v)
#         return (r, g, b)

#     def Verifica_Cor(x,y,z):
#         #(x, y, z) = cor3.value(0), cor3.value(1), cor3.value(2)
#         x = x/1023
#         y = y/1023
#         z = z/1023
        
#         (h, s, v) = convertHSV(x, y, z)
        
#         s = 0.8
#         v = 1
#         (r, g, b) = convertRGB(h, s, v)
        
#         r = r * 255
#         g = g * 255
#         b = b * 255
        
#         #Codigo Lucas
#         colors = {
#             "1": "#000000", #Black
#             "5": "#FF0000", #Red
#             "4": "#FFFF00", #Yellow
#             "3": "#00FF00", #Green
#             "2": "#0000FF", #Blue
#             "6": "#FFFFFF" #White
#         }

#         def rgbFromStr(s):
#                 r, g, b = int(s[1:3],16), int(s[3:5], 16),int(s[5:7], 16)  
#                 return r, g, b  

#         def findNearestColorName(color, Map):  
#             (R,G,B) = color
#             mindiff = None
#             for d in Map:  
#                 r, g, b = rgbFromStr(Map[d])  
#                 diff = abs(R-r) * 256 + abs(G-g) * 256 + abs(B-b) * 256   
#                 if mindiff is None or diff < mindiff:  
#                     mindiff = diff  
#                     mincolorname = d  
#             return mincolorname    

#         return findNearestColorName((r, g, b), colors)

#     while (Sensor_Cor[0].value() != 5 and Sensor_Cor[1].value() != 5):
#         m1.run_forever(speed_sp=180)
#         m2.run_forever(speed_sp=180)
#         print(Sensor_Cor[0].value())
        
#     m1.stop(stop_action="brake")
#     m2.stop(stop_action="brake")
#     time.sleep(1.5)
#     m1.run_to_rel_pos(position_sp=360,speed_sp=180,stop_action="brake")
#     m2.run_to_rel_pos(position_sp=360,speed_sp=180,stop_action="brake")
#     time.sleep(1.5)
#     Sensor_Cor[0].mode = 'RGB-RAW'
#     Sensor_Cor[1].mode = 'RGB-RAW'

#     color = Verifica_Cor(Sensor_Cor[0].value(0), Sensor_Cor[0].value(1), Sensor_Cor[0].value(2))
#     print(color)
#     Sensor_Cor[0].mode = 'COL-COLOR'
#     Sensor_Cor[1].mode = 'COL-COLOR'
#     time.sleep(0.8)

def giraRobo(graus, tempo = 2): #90 > 0: direita else: esquerda
    razaoRobo = 5.25 / 3.0

    if graus > 0:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=280,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=280,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=-(razaoRobo*(graus*-1)),speed_sp=280,stop_action="brake")
        m2.run_to_rel_pos(position_sp=(razaoRobo*(graus*-1)),speed_sp=280,stop_action="brake")
    if tempo != 0:
        time.sleep(tempo)

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

def scan_gasoduto():
    tempo_inicio, tempos_pista, anterior_leitura, tempo_final = -1, [], -1, -1
    #tempo_dez, tempo_quinze, tempo_vinte = 0,0,0
    m1.run_forever(speed_sp=150)
    m2.run_forever(speed_sp=150)
    while (ir.value() > 30):
        m1.run_forever(speed_sp=180)
        m2.run_forever(speed_sp=180)
    giraRobo(-90)
    time.sleep(.8)
    if (Sensor_Ultrassonico[0].value() > 36 or Sensor_Ultrassonico[1].value() > 36):
        m1.stop_action("brake")
        m2.stop_action("brake")
        
        m1.run_timed(time_sp=70, speed_sp=-180, stop_action="brake")
        m2.run_timed(time_sp=70, speed_sp=-180, stop_action="brake")
        
        m1.stop_action("brake")
        m2.stop_action("brake")

        giraRobo(180)
        if len(tempos_pista) > 1:
            tempos_pista.append(time.time())
    elif anterior_leitura == -1:
        tempos_pista.append(time.time()) 
        anterior_leitura = ir.value()
    elif (ir.value() - anterior_leitura) > 20: #Descobre um vao
        tempos_pista.append(time.time())
        anterior_leitura = ir.value()
        if tempo_inicio == -1:
            tempo_inicio = time.time()
    elif (ir.value() - anterior_leitura) < 20: #Vao fechou
        tempos_pista.append(time.time())
        tempo_final = time.time()
        anterior_leitura = ir.value()
        
