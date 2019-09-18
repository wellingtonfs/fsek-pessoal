#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
import socket, time
import math

ir = InfraredSensor('in1')
ir.mode = 'IR-PROX'

ir2 = InfraredSensor('in2')
ir2.mode = 'IR-PROX'

tc = TouchSensor('in4')

'''cor = ColorSensor('in3')
cor.mode = 'RGB-RAW
'''

Verificar_Conexao = True
tt = 0
cont = 0
while True:
    try:
        while True:
            Servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Servidor.connect(('169.255.168.150', 3562))
            if Verificar_Conexao:
                cont += 1
                print("Conectado" + str(cont))
                Verificar_Conexao = False

            #print("%d --- %d" %(ir.value() %ir2.value()))

            Str_Env = "%d,%d," %(ir.value(), ir2.value())
            Str_Env += str(tc.value())

            if (time.time() - tt) > 0.5:
                print(Str_Env)
                tt = time.time()

            '''if (time.time() - tt) > 0.5:
                print("%d  -  %d" %(ir2.value(), cor.value()))
                tt = time.time()'''

            St = Str_Env.encode('utf-8')

            Servidor.send(St)
            time.sleep(0.05)

        Servidor.close()
            
    except Exception as e:
        print(e)
        Verificar_Conexao = True
        