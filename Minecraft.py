#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import time, socket
import math
import colorsys

m1 = LargeMotor('outD') #Esquerdo
m2 = LargeMotor('outC') #Direito

Sensor_Cor = [ColorSensor('in1'), ColorSensor('in2')] #1 = Esquerdo, 2 = Direito

Sensor_Cor[0].mode = 'COL-COLOR'
Sensor_Cor[1].mode = 'COL-COLOR'

def VerificacaoCor():
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

    while (Sensor_Cor[0].value() != 5 and Sensor_Cor[1].value() != 5):
        m1.run_forever(speed_sp=180)
        m2.run_forever(speed_sp=180)
        print(Sensor_Cor[0].value())
        
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(1.5)
    m1.run_to_rel_pos(position_sp=360,speed_sp=180,stop_action="brake")
    m2.run_to_rel_pos(position_sp=360,speed_sp=180,stop_action="brake")
    time.sleep(1.5)
    Sensor_Cor[0].mode = 'RGB-RAW'
    Sensor_Cor[1].mode = 'RGB-RAW'

    color = Verifica_Cor(Sensor_Cor[0].value(0), Sensor_Cor[0].value(1), Sensor_Cor[0].value(2))
    print(color)
    Sensor_Cor[0].mode = 'COL-COLOR'
    Sensor_Cor[1].mode = 'COL-COLOR'
    time.sleep(0.8)


