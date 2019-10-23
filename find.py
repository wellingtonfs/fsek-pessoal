
from ev3dev.ev3 import *

from threading import *
from ev3dev2.motor import OUTPUT_C, OUTPUT_D, MoveTank
import time, socket, json
import math

tank = MoveTank(OUTPUT_D, OUTPUT_C)
m1 = LargeMotor('outD') #Direito
m2 = LargeMotor('outC') # Esquerdo
m3 = MediumMotor('outB')
m4 = MediumMotor('outA')
us = UltrasonicSensor('in3') #Direto
us2 = UltrasonicSensor('in4') #esquerdo
gy = GyroSensor('in1')
us3 = UltrasonicSensor('in2')
#Sensor_Cor = [ColorSensor('in2'), ColorSensor('in1')] #2 = Esquerdo, 1 = Direito

us.mode = 'US-DIST-CM'
us2.mode = 'US-DIST-CM'
us3.mode = 'US-DIST-CM'
gy.mode = 'GYRO-ANG'
#Sensor_Cor[0].mode = 'COL-COLOR'
#Sensor_Cor[1].mode = 'COL-COLOR'

class Communication(Thread):
    def __init__(self):
        self.sc_value = 0
        self.sc2_value = 0
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(('169.255.168.150', 3571))
                    s.listen()
                    while True:
                        conn, addr = s.accept()
                        with conn:
                            while True:
                                data = conn.recv(1024)

                                if not data:
                                    break

                                Sedex = json.loads(data.decode())
                                self.sc_value = Sedex['sc']
                                self.sc2_value = Sedex['sc2']

            except Exception as e:
                print(e)
                time.sleep(0.5)

Comm = Communication()
Comm.daemon = True
Comm.start()

def Encontrar_Pos():
    while True:#Comm.ir_value
        if Sensor_Cor[0].value() == 1 or Sensor_Cor[1].value() == 1: #Se achar Preto
            Al = alinhar(1)
            if Al == 1:
                Emergencia(80)
            elif Al == 2:
                Emergencia(-80)
            else:
                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")
                return 0
        elif Sensor_Cor[0].value() == 3 or Sensor_Cor[1].value() == 3: #Se achar Verde
            Emergencia(180)
        elif 40 < us.value() < 400:
            Emergencia(90)
        elif 40 < us2.value() < 400:
            Emergencia(-90)

        m1.run_forever(speed_sp=300)
        m2.run_forever(speed_sp=300)
 
def giraRobo(graus, sentido):
    razaoRobo = (6.3)/3
    if sentido:
        m2.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=180,stop_action="brake")    
        m2.run_to_rel_pos(position_sp=(-razaoRobo*graus),speed_sp=180,stop_action="brake")
    time.sleep(2)


def alinhar(c): #Essa função alinha o lego a uma cor especifica c.
    print("entrei no alinhar")
    if Comm.sc_value == c and Comm.sc2_value == c:
        return 0
    while True:
        if Comm.sc_value == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while Comm.sc_value == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            #m1.run_forever(speed_sp=-150)
            m2.run_forever(speed_sp=100)
            while Comm.sc2_value != c:
                if Comm.sc2_value == 0:
                    return 1
                if Comm.sc_value != c:
                    m2.stop(stop_action="brake")
                    m1.run_forever(speed_sp=70)
                else:
                    m1.stop(stop_action="brake")
                    m2.run_forever(speed_sp=100)
                if 70 < us2.value() < 400:
                    return 2
            break

        if Comm.sc2_value == c:
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            while Comm.sc2_value == c:
                m1.run_forever(speed_sp=-50)
                m2.run_forever(speed_sp=-50)
            m1.stop(stop_action="brake")
            m2.stop(stop_action="brake")
            m1.run_forever(speed_sp=100)
            #m2.run_forever(speed_sp=-150)
            while Comm.sc_value != c:
                if Comm.sc_value == 0:
                    return 1
                if Comm.sc2_value != c:
                    m1.stop(stop_action="brake")
                    m2.run_forever(speed_sp=70)
                else:
                    m1.run_forever(speed_sp=100)
                    m2.stop(stop_action="brake")
                if 70 < us.value() < 400:
                    return 1
            break

    m1.run_forever(speed_sp=250)
    m2.run_forever(speed_sp=250)
    time.sleep(1)
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    return 0

giraRobo(180, True)
time.sleep(1)
while(True):
   # m1.run_forever(speed_sp=60)
    #m2.run_forever(speed_sp=60)
    print(Comm.sc2_value)
    alinhar(1)