#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *
import socket, time

while True:
    try:
        Cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Cliente.bind(('169.255.168.150', 3549))
        Cliente.listen(1)

        while True:
            Msg, Endereco_Cliente = Cliente.accept()
            Dados = str(Msg.recv(1024).decode()).split(",")
            print(Dados)

        Cliente.close()
    except Exception as e:
        print(e)
        time.sleep(1)
