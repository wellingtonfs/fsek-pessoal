#!/usr/bin/env python3
from ev3dev.ev3 import *
import time

Sensor_Cor = [ColorSensor('in3'), ColorSensor('in4')]

Sensor_Cor[0].mode = 'COL-COLOR'
Sensor_Cor[1].mode = 'COL-COLOR'

while True:
    string = "c1:%d\nc2:%d\n--\n" %(Sensor_Cor[0].value(), Sensor_Cor[1].value())
    print(string)
    time.sleep(0.5)