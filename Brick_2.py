#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import socket, time
import math

ir = InfraredSensor('in1')
ir.mode = 'IR-PROX'

ir2 = InfraredSensor('in2')
ir2.mode = 'IR-PROX'

cor3 = ColorSensor('in3')
cor3.mode = 'RGB-RAW'

class Communication(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        Verificar_Conexao = True
        tt = 0
        cont = 0
        while True:
            try:
                while True:
                    Servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    Servidor.connect(('169.255.168.153', 3563))
                    if Verificar_Conexao:
                        cont += 1
                        print("Conectado" + str(cont))
                        Verificar_Conexao = False

                    #print("%d --- %d" %(ir.value() %ir2.value()))

                    Str_Env = "%d,%d,%d,%d,%d" %(ir.value(), ir2.value(), cor3.value(0), cor3.value(1), cor3.value(2))

                    if (time.time() - tt) > 0.5:
                        print("%d  -  %d" %(ir2.value(), cor.value()))
                        tt = time.time()

                    St = Str_Env.encode('utf-8')

                    Servidor.send(St)
                    Servidor.close()
                    time.sleep(1)

                Servidor.close()
                    
            except Exception as e:
                print(e)
                Verificar_Conexao = True

Comm = Communication()
Comm.daemon = True
Comm.start()

while True:
    pass

        