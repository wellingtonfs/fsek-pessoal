#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import socket, time, json

ir = InfraredSensor('in1')
ir.mode = 'IR-PROX'

m1 = LargeMotor('outD')
m2 = LargeMotor('outA')

cont = 0
arq = open("Dados.txt","w")
arq.write("Leituras: \n\n")
arq.close()

def Salvar(x):
    global cont
    arq = open("Dados.txt","a")
    ss = "%d,%d\n" %(x, cont)
    arq.write(ss)
    arq.close()
    cont += 1

class Communication(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(('169.255.168.151', 3562))
                
                    while True:

                        Sedex = {
                            "IR1" : ir.value()
                        }

                        s.send(json.dumps(Sedex).encode())
                        time.sleep(0.5)
            except Exception as e:
                print(e)
                s.close()
                time.sleep(0.5)

comm = Communication()
comm.daemon = True
comm.start()

while True:
    Salvar(ir.value())
    m1.run_forever(speed_sp=70)
    m2.run_forever(speed_sp=70)