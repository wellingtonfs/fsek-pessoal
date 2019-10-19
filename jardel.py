#!/usr/bin/env python3
# so that script can be run from Brickman
import termios, tty, sys
from ev3dev.ev3 import *
import colorsys               

# attach large motors to ports B and C, medium motor to port A
motor_left = LargeMotor('outC')
motor_right = LargeMotor('outD')

Sensor_Cor = [ColorSensor('in2'), ColorSensor('in1')] #1 = Esquerdo, 2 = Direito
Sensor_Cor[0].mode = 'COL-COLOR'
Sensor_Cor[1].mode = 'COL-COLOR'

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

# motor_a = MediumMotor('outA')
# motor_b = MediumMotor('outB')

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    ch = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch

def forward():
    motor_left.run_forever(speed_sp=200)
    motor_right.run_forever(speed_sp=200)

#==============================================

def back():
    motor_left.run_forever(speed_sp=-200)
    motor_right.run_forever(speed_sp=-200)

#==============================================

def left():
    motor_left.run_forever(speed_sp=-200)
    motor_right.run_forever(speed_sp=200)

#==============================================

def right():
    motor_left.run_forever(speed_sp=200)
    motor_right.run_forever(speed_sp=-200)

#==============================================

def stop():
    motor_left.run_forever(speed_sp=0)
    motor_right.run_forever(speed_sp=0)
#     motor_a.run_forever(speed_sp=0)
#     motor_b.run_forever(speed_sp=0)
# #==============================================

# def up():
#     motor_a.run_forever(speed_sp=200)
#     motor_b.run_forever(speed_sp=-200)

# def down():
#     motor_a.run_forever(speed_sp=-200)
#     motor_b.run_forever(speed_sp=200)

while True:
    if (Sensor_Cor[0].value() == Sensor_Cor[1].value()):
        Sensor_Cor[0].mode = 'RGB-RAW'
        Sensor_Cor[1].mode = 'RGB-RAW'
        (x,y,z) = (Sensor_Cor[0].value(0),Sensor_Cor[0].value(1),Sensor_Cor[0].value(2))
        color = Verifica_Cor(x,y,z)
        Sensor_Cor[0].mode = 'COL-COLOR'
        Sensor_Cor[1].mode = 'COL-COLOR'
        print(color)
    k = getch()
    print(k)
    if k == 's':
        back()
    if k == 'w':
        forward()
    if k == 'd':
        right()
    if k == 'a':
        left()
    if k == ' ':
        stop()
    if k == 'o':
        up()
    if k == 'p':
        down()
    if k == 'q':
        exit()