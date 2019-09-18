#!/usr/bin/env python3
from ev3dev.ev3 import *
from threading import *
import time, socket

m1 = LargeMotor('outD')
m2 = LargeMotor('outC')
Estado = -1

arq = open("ll.txt", "w")
arq.write("Leituras:\n\n")
arq.close()

def salvar(msg):
    arq = open("ll.txt", "a")
    arq.write(msg)
    arq.close()
    
class Communication(Thread):
    def __init__(self):
        self.ir_value = 0
        self.ir2_value = 0
        self.tc = ' '
        Thread.__init__(self)

    def run(self):
        global Estado
        while True:
            try:
                Cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                Cliente.bind(('169.255.168.150', 3562))
                Cliente.listen(1)

                while True:
                    Msg, Endereco_Cliente = Cliente.accept()
                    Dados = str(Msg.recv(1024).decode()).split(",")
                    self.ir_value = int(Dados[0])
                    self.ir2_value = int(Dados[1])
                    self.tc = Dados[2]
                    if Estado == -1:
                        print("Conectado")
                        Estado = 0

                Cliente.close()
            except Exception as e:
                print(e)
                time.sleep(1)

Comm = Communication()
Comm.daemon = True
Comm.start()

temp = 0
a = False

while True:
    if Estado == 0:
        if Comm.tc == '1':
            a = True
            m1.run_forever(speed_sp=70)
            m2.run_forever(speed_sp=-70)
            str_p = "%d\n" %Comm.ir_value
            salvar(str_p)
            temp = time.time()
        else:
            if a:
                salvar("\n\n--------\n\n")
                a = False
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")