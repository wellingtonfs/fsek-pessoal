#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import time, socket
import math
import colorsys

cor3 = ColorSensor('in1')
cor3.mode = 'RGB-RAW'

def convertHSV(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return (h, s, v)

def convertRGB(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (r, g, b)

def Verifica_Cor():
    (x, y, z) = cor3.value(0), cor3.value(1), cor3.value(2)
    x = x/1023
    y = y/1023
    z = z/1023
    #print(x,y,z)
    #print("\n")
    (h, s, v) = convertHSV(x, y, z)
    #print(h,s,v)
    #print("\n")
    s = 0.8
    v = 1
    (r, g, b) = convertRGB(h, s, v)
    #print(r,g,b)
    #print("\n")
    r = r * 255
    g = g * 255
    b = b * 255
    
    #Codigo Lucas
    color_name = ""

    colors = {
        "black": "#000000",
        "red": "#FF0000",
        "yellow": "#FFFF00",
        "green": "#00FF00",
        "blue": "#0000FF",
        "white": "#FFFFFF"
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

    color = findNearestColorName((r, g, b), colors)
    print(color, " - ", r, g, b)
    #print("\n")

while True: 
    Verifica_Cor()
    #print(color)
    time.sleep(5)
    
    