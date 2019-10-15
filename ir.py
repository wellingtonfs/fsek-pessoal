#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import socket, time
import math

m1 = LargeMotor('outD') #Esquerdo
m2 = LargeMotor('outC') #Direito

m1.run_forever(speed_sp=300)
m2.run_forever(speed_sp=300)