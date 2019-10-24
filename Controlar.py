#!/usr/bin/env python3
# so that script can be run from Brickman
import termios, tty, sys, time
from ev3dev.ev3 import *
from threading import *

# attach large motors to ports B and C, medium motor to port A
motor_right = LargeMotor('outD')
motor_left = LargeMotor('outC')

#gy = GyroSensor('in1')
#gy.mode = 'GYRO-ANG'

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    ch = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch

def forward():
    motor_left.run_forever(speed_sp=400)
    motor_right.run_forever(speed_sp=400)

#==============================================

def back():
    motor_left.run_forever(speed_sp=-400)
    motor_right.run_forever(speed_sp=-400)

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
#==============================================

while True:
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
    if k == 'q':
        exit()