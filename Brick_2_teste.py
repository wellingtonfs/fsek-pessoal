#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
from threading import *
import socket, time, json, math

ir = InfraredSensor('in3')
ir.mode = 'IR-PROX'

'''
ir = UltrasonicSensor('in1')
ir.mode = 'US-DIST-CM'
'''
 
m1 = LargeMotor('outD')
m2 = LargeMotor('outC')

arq = open("Dados.txt","w")
arq.write("Leituras: \n\n")
arq.close()

vetor = []

def Salvar(x):
    arq = open("Dados.txt","a")
    ss = "%.2f %f\n" %(x[0], x[1])
    arq.write(ss)
    arq.close()

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
            except:
                #print(e)
                s.close()
                time.sleep(0.5)

comm = Communication()
comm.daemon = True
comm.start()

def Modulo(x):
    if x < 0:
        return x * -1
    return x 

def Tratar_Vetor(vetor):
    menor = [100, 0]
    for i in range(len(vetor)):
        if menor[0] > vetor[i][0]:
            menor[0] = vetor[i][0]
            menor[1] = i

    vet = []
    tempo = 0
    if (len(vetor) - menor[1]) < (menor[1] - 0):
        for i in range(menor[1]):
            vet.append(vetor[i][0])
            tempo = vetor[menor[1]][1] - vetor[0][1]
    else:
        for i in range(menor[1], len(vetor)):
            vet.append(vetor[i][0])
            tempo = vetor[len(vetor)-1][1] - vetor[menor[1]][1]
    return [vet, tempo]

def Angulo_Reta(pontos):
    pts_temp = Tratar_Vetor(pontos)

    p1 = pts_temp[0][0]
    p2 = pts_temp[0][len(pts_temp[0])-1]

    cateto1 = 34*2
    cateto2 = Modulo(p2 - p1)
    hipotenusa = math.sqrt(((cateto1**2) + (cateto2**2)))

    ang = Modulo(int(math.acos((cateto1 / hipotenusa)) * 57.2958))
    print("%d" %ang)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(10)

pegar_tempo = 0
ent = True

while True:
    x = ir.value()
    if ent:
        if x < 66:
            t = time.time()
            if pegar_tempo == 0:
                pegar_tempo = t
            Salvar([x, t])
            vetor.append([x, t])
        else:
            if pegar_tempo != 0:
                Angulo_Reta(vetor)
                ent = False
    m1.run_forever(speed_sp=50)
    m2.run_forever(speed_sp=50)