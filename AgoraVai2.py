#!/usr/bin/env python3
#coding: utf-8
from ev3dev.ev3 import *

from threading import *
from ev3dev2.motor import OUTPUT_C, OUTPUT_D, MoveTank
import time, socket, json
import math

tank = MoveTank(OUTPUT_C, OUTPUT_D)

m1 = LargeMotor('outD') #Direito
m2 = LargeMotor('outC') # Esquerdo
m3 = MediumMotor('outB')
m4 = MediumMotor('outA')
# us = UltrasonicSensor('in3') #Direto
# us2 = UltrasonicSensor('in4') #esquerdo
sc = ColorSensor('in1')
sc2 = ColorSensor('in2')

sc.mode = 'COL-COLOR'
sc2.mode = 'COL-COLOR'

ubL = 0

ub = UltrasonicSensor('in4')
ub.mode = 'US-DIST-CM'

gy = GyroSensor('in3')
# us3 = UltrasonicSensor('in4')
#Sensor_Cor = [ColorSensor('in2'), ColorSensor('in1')] #2 = Esquerdo, 1 = Direito

tamanhoTubo = 0
coresComTubo = [5, 4, 2]

gy.mode = 'GYRO-ANG'

controleCor = False
#Sensor_Cor[0].mode = 'COL-COLOR'
#Sensor_Cor[1].mode = 'COL-COLOR'

class Communication(Thread):
    def __init__(self):
        self.uc_value = 0
        self.ut_value = 0
        self.ir_value = 0
        self.uf_value = 0
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(('169.255.168.150', 3572))
                    s.listen()
                    while True:
                        conn, addr = s.accept()
                        with conn:
                            while True:
                                data = conn.recv(1024)

                                if not data:
                                    break

                                Sedex = 0
                                try:
                                    Sedex = json.loads(data.decode())
                                except:
                                    st = data.decode()
                                    for i in range(len(st)):
                                        if st[i] == '}':
                                            Sedex = json.loads(st[0:i+1])
                                            break
                                            
                                self.uc_value = Sedex['uc']
                                self.ut_value = Sedex['ut']
                                self.ir_value = Sedex['ir']
                                self.uf_value = Sedex['uf']
            except Exception as e:
                print(e)
                time.sleep(0.5)

Comm = Communication()
Comm.daemon = True
Comm.start()

def Testar_Dist():
    lego.parar()

    def g(valor, a):
        if a:
            m1.run_to_rel_pos(position_sp=-valor, speed_sp=100, stop_action="brake")
            m2.run_to_rel_pos(position_sp=valor, speed_sp=100, stop_action="brake")
        else:
            m1.run_to_rel_pos(position_sp=valor, speed_sp=100, stop_action="brake")
            m2.run_to_rel_pos(position_sp=-valor, speed_sp=100, stop_action="brake")

    valores = []
    somar = 0
    for i in [True, False, False, True]:
        u = ub.value()
        valores.append(u)
        somar += u
        g(30, i)
        time.sleep(0.5)

    if all(i > 2300 for i in valores) or all(i < 2300 for i in valores):
        print("t_dist 1: ", (somar / int(len(valores))))
        return (somar / int(len(valores)))
    else:
        somar = [0, 0]
        for i in valores:
            if i < 2300:
                somar[0] += i
                somar[1] += 1
        print("t_dist 2: ", (somar[0] / somar[1]))
        return (somar[0] / somar[1])

class andar(Thread):
    def __init__(self):
        self.andando = False
        self.parando = False
        self.vel = 200
        self.ang = 0.2
        self.parado = False
        Thread.__init__(self)

    def run(self):
        global ubL

        while True:
            if self.andando:
                speed1, speed2 = self.vel, self.vel
                anterior = self.ang
                while self.parando == False:
                    if self.ang == 0:
                        m1.run_forever(speed_sp=self.vel)
                        m2.run_forever(speed_sp=self.vel)
                    else:
                        leitura = ubL
            
                        if leitura > 2548:
                            leitura = self.ang
                        
                        print(leitura)

                        if leitura < self.ang:
                            variacao = (self.ang - leitura)
                            if variacao > 70:
                                variacao = 70
                            if self.vel > 0:
                                speed2 = self.vel + (variacao/3)
                            else:
                                speed2 = self.vel - (variacao/3)
                            speed1 = self.vel
                        elif leitura > self.ang:
                            variacao = (leitura - self.ang) 
                            if variacao > 70:
                                variacao = 70
                            if self.vel > 0:
                                speed1 = self.vel + (variacao/3)
                            else:
                                speed1 = self.vel - (variacao/3)
                            speed2 = self.vel
                        else:
                            speed1, speed2 = self.vel, self.vel

                        m1.run_forever(speed_sp=speed2)
                        m2.run_forever(speed_sp=speed1)

                m1.stop(stop_action="brake")
                m2.stop(stop_action="brake")

                self.andando = False
                self.parando = False
                self.ang = 0
                self.parado = False

    def andar(self, speed = -150, dist = 0):
        while self.parado:
            pass
        self.andando = True
        self.parando = False
        self.vel = speed
        self.ang = dist

    def parar(self):
        if self.andando:
            self.parando = True
            self.parado = True

    def andar_tempo(self, speed = 200, dist = 0, tempo = 0):
        self.parar()
        while self.parado:
            pass
        t = time.time()
        while (time.time() - t) <= tempo:
            self.andar(speed=speed, dist=dist)
        self.parar()

lego = andar()
lego.daemon = True
lego.start()

'''
def Encontrar_Pos():
    while True:
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
        elif 50 < us.value() < 300:
            print ("Caindo")
            print (us.value())
            Emergencia(90)
        elif 50 < us2.value() < 300:
            print ("Caindo")
            print (us2.value())
            Emergencia(-90)

        m1.run_forever(speed_sp=300)
        m2.run_forever(speed_sp=300)
'''
def Emergencia(graus):
    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(0.5)

    m1.run_to_rel_pos(position_sp=-400,speed_sp=150,stop_action="brake")
    m2.run_to_rel_pos(position_sp=-400,speed_sp=150,stop_action="brake")
    time.sleep(3)
    giraRobo(graus)
    m1.run_forever(speed_sp=300)
    m2.run_forever(speed_sp=300)
'''
def gyro(an):
    baseAngle = gy.value()

    mdiff.turn_left(SpeedRPM(40), an)
    time.sleep(0.5)

    angle = abs(gy.value() - baseAngle)
    diffAng = angle - an

    if(diffAng < 0):
        mdiff.turn_left(SpeedRPM(40), abs(diffAng))
    else:
        mdiff.turn_right(SpeedRPM(40), abs(diffAng))
    time.sleep(2)
'''
def giraRobo(graus, tempo = 2): #90 > 0: direita else: esquerda
    razaoRobo = 5.25 / 3.0

    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(0.3)

    if graus > 0:
        m1.run_to_rel_pos(position_sp=(razaoRobo*graus),speed_sp=280,stop_action="brake")
        m2.run_to_rel_pos(position_sp=-(razaoRobo*graus),speed_sp=280,stop_action="brake")
    else:
        m1.run_to_rel_pos(position_sp=-(razaoRobo*(graus*-1)),speed_sp=280,stop_action="brake")
        m2.run_to_rel_pos(position_sp=(razaoRobo*(graus*-1)),speed_sp=280,stop_action="brake")
    if tempo != 0:
        time.sleep(tempo)

def alinhar(c): #Essa função alinha o lego a uma cor especifica c.
    if sc.value() == c and sc2.value() ==  c:
        if ruido(c):
            return True

    while True:
        if sc.value() == c:
            tank.stop()

            while sc.value() == c:
                tank.on(-10, -10)

            tank.stop()
            tank.on(10, 0)

            while sc2.value() != c:
                tank.on(0, 10)
            
            while sc2.value() == c:
                tank.on(0, -10)
                
            break

        if sc2.value() == c:
            tank.stop()

            while sc2.value() == c:
                tank.on(-10, -10)

            tank.stop()
            tank.on(0, 10)

            while sc.value() != c:
                tank.on(10, 0)

            while sc.value() == c:
                tank.on(-10, 0)

            break

    tank.stop()

    return False

def Mov_Garra_Analog(Sentido, Pos): 
    if Sentido:
        m3.run_to_rel_pos(position_sp=((-1)*Pos),speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
        time.sleep(1)
    else:
        m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
        m4.run_to_rel_pos(position_sp=((-1)*Pos),speed_sp=150,stop_action="brake")
        time.sleep(1)

def alinhar_ultra(): #Essa função alinha o lego a uma cor especifica c.
    if us.value() > 100 and us2.value() > 100:
        return 0
    if us.value() > 100:
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        while us.value() > 100:
            m1.run_forever(speed_sp=-50)
            m2.run_forever(speed_sp=-50)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        #m1.run_forever(speed_sp=-150)
        m2.run_forever(speed_sp=100)
        while us2.value() < 100:
            pass

    if us2.value() > 100:
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        while us2.value() > 100:
            m1.run_forever(speed_sp=-50)
            m2.run_forever(speed_sp=-50)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        m1.run_forever(speed_sp=100)
        #m2.run_forever(speed_sp=-150)
        while us.value() < 100:
            pass

    m1.stop(stop_action="brake")
    m2.stop(stop_action="brake")
    time.sleep(1)
    return 0

def Mov_Garra_Sensor(Sentido, Pos): #0 = descer; 1 = subir;
    if Sentido: 
        if (Comm.uf_value < 400):
            while (Comm.uf_value < 100):
                m3.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
                m4.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
                time.sleep(0.5)
    else: 
        while (Comm.uf_value > 45):
            m3.run_to_rel_pos(position_sp=Pos,speed_sp=150,stop_action="brake")
            m4.run_to_rel_pos(position_sp=(-1)*Pos,speed_sp=150,stop_action="brake")
            time.sleep(0.5)
    time.sleep(2)

def rotateTo(degrees, speed = 10, linearSpeed = 0):
    # Clockwise
    angleBase = gy.value()

    if degrees > 0:
        left_speed = speed + linearSpeed
        right_speed = -speed + linearSpeed
    else:
        left_speed = -speed + linearSpeed
        right_speed = speed + linearSpeed

    degrees = abs(degrees)

    tank.on(left_speed, right_speed)
    while abs(gy.value() - angleBase) <= degrees:
        pass
    tank.stop()

def rotateCm(cm, speed = 15):
    degrees = cm * 360 / 17.6

    positionBase = m1.position

    if(cm < 0):
        speed = -speed

    tank.on(speed, speed)
    
    while abs(m1.position - positionBase) <= abs(degrees):
        pass
    tank.stop()

def Cano_Suporte(pos):
    m3.stop()
    m4.stop()
    lego.andar_tempo(speed=100, tempo=4)
    m3.run_to_rel_pos(position_sp=180,speed_sp=150,stop_action="brake")
    m4.run_to_rel_pos(position_sp=-180,speed_sp=150,stop_action="brake")

    time.sleep(3)

    m1.run_to_rel_pos(position_sp=-pos,speed_sp=250,stop_action="brake")
    m2.run_to_rel_pos(position_sp=-pos,speed_sp=250,stop_action="brake")
    time.sleep(2)

def Entregar_Tubo(tempo = 0, tam=0):
    lego.parar()
    if tam == 10:
        lego.andar_tempo(speed=150, tempo=(tempo - 1.2))
    elif tam == 15:
        lego.andar_tempo(speed=150, tempo=(tempo - 1.5))
    else:
        lego.andar_tempo(speed=150, tempo=(tempo - 2))
    rotateTo(90)
    print("colocando o tubo")
    Cano_Suporte(200)
    rotateTo(-90)
    lego.andar_tempo(speed=-150, tempo=tempo)

def c_tubo(tam_tubo):
    global ubL
    Estado = 0
    var_est = False
    while True:
        if Estado == 0: #chegar no gasoduto pela primeira vez
            print("Esperando comunicacao..")
            while Comm.ut_value == 0:
                pass

            lego.andar()

            print("indo ate o gasoduto")
            while Comm.ut_value > 150:
                print(Comm.ut_value)

            lego.parar()
            print("saiu do while de ir ate o gasoduto")
            rotateTo(90)

            Estado = 1
            
        elif Estado == 1: #andar paralelo ao gasoduto
            ubL = ub.value()
            lego.andar(dist=130)

            time_vao = 0
            time_entrada = 0

            print("Entrou while procurar cano")
            while Comm.ut_value > 110: #verificar queda dps
                try:
                    ubL = ub.value()
                except Exception as e:
                    print(e)

                if Comm.uc_value > 200 and time_entrada == 0:
                    print("Inicio tubo")
                    time_entrada = time.time()
                elif Comm.uc_value < 200 and time_entrada != 0:
                    tempo_dif = (time.time() - time_entrada)
                    if tempo_dif > 1.1:
                        if tam_tubo == 10 or (tam_tubo == 15 and tempo_dif > 2) or (tam_tubo == 20 and tempo_dif > 2.5):
                            Entregar_Tubo(tempo=tempo_dif, tam=tam_tubo)
                            return True
                        else:
                            print("Nao cabe", tempo_dif)
                    else:
                        print("vao falso", tempo_dif)
                    time_entrada = 0

                if ubL > 200 and time_vao == 0:
                    time_vao = time.time()
                elif time_vao != 0 and (time.time() - time_vao) > 0.5:
                    if ubL > 200 and var_est:
                        Estado = 3
                        break
                    else:
                        time_vao = 0

                if Comm.ir_value > 21:
                    lego.parar()
                    Estado = 4
                    break

            if Estado == 1:
                Estado = 2

            print("Saiu while procurar cano")

        elif Estado == 2: #dobrar a direita
            print("Entrou em dobrar 1")
            lego.parar()
            rotateTo(90)
            Estado = 1
            var_est = True

        elif Estado == 3: #dobrar a esquerda
            print("Entrou em dobrar 2")
            lego.andar_tempo(speed=-150, tempo=3)
            rotateTo(-90)

            lego.andar(dist=130)
            while ub.value() > 200:
                pass

            lego.parar()

            Estado = 1
            var_est = False
            print("Saiu andar 2")

        elif Estado == 4: #final do gasoduto e fim da funcao
            print("Fim da funcao")
            return False

def walkUntilDistance(distance, speed = 10, limit = 0):
    tank.on(speed, speed)
    count = 0
    while Comm.uf_value > distance:
        print(Comm.uf_value, count, limit)
        count += 1
        if(limit != 0 and count > limit):
            return False
        pass
    tank.stop()
    return True

def walkUntilColor(color, speed = 10, limit = 0):
    tank.on(speed, speed)
    count = 0

    while True:
        while sc.value() != color and sc2.value() != color:
            count += 1
            if(limit != 0 and count > limit):
                return False

        # se nã0 passar no ruido continua andando
        if ruido(color):
            break
        else:
            tank.on(speed, speed)

    tank.stop()

    print("Chegou na cor:", color)
    return True

def grabTube():
    #fica se mexendo
    rotateTo(10)

    for i in range(0, 1):
        rotateTo(-20, speed = 5 , linearSpeed = 5)
        rotateTo(20, speed = 5, linearSpeed = 5)

        if(Comm.uf_value < 80):
            break

    rotateTo(-10)
    #avança para pegar o tubo

    #retorna se pegou ou não
    if(Comm.uf_value < 80):
        tank.on_for_degrees(10, 10, 90)
        return True

    return False

def alignWithTube(degrees, count = 0, test = True):
    if(count == 5):
        tank.on_for_degrees(10, 10, -100 * count)
        backOriginalPosition(0)
        PegarTubo(count = 2)
        return "break"

    tube = {
        "angle": 0,
        "dist": 500
    }

    loopSize = int(degrees/5)
    loopCal = int(loopSize/2)

    startAngle = gy.value()

    for i in range(0, loopSize):
        print(tube)
        ultra = Comm.uf_value if Comm.uf_value < 500 else 500

        # fazer ele se mecher e ler diversar distancias dentro desse 10cm e  calcular a media
        if(ultra < tube['dist']):
            tube['angle'] = i*5 #Angulo Atual
            tube['dist'] = ultra

        if(i == loopCal): #recalibra
            rotateTo(startAngle + (degrees/2) - gy.value())

        rotateTo(5, speed= 5)


    rotateTo(-degrees)
    rotateTo(startAngle - gy.value())

    startAngle = gy.value()
    for i in range(0, loopSize):
        print(tube)
        ultra = Comm.uf_value if Comm.uf_value < 500 else 500

        # fazer ele se mecher e ler diversar distancias dentro desse 10cm e  calcular a media
        if(ultra < tube['dist']):
            tube['angle'] = i*-5 #Angulo Atual
            tube['dist'] = ultra

        if(i == loopCal): #recalibra
            rotateTo(startAngle - (degrees/2) - gy.value())

        rotateTo(-5, speed= 5)

    # agora ja sei o angulo onde o tubo de encontra
    rotateTo(degrees)
    rotateTo(startAngle - gy.value())

    if(tube['dist'] == 500 and test):
        tank.on_for_degrees(10, 10, 180)
        return alignWithTube(90, count + 1)

    if tube['dist'] == 500 and not test:
        tank.on_for_degrees(10, 10, -180)
        return alignWithTube(60, count + 1)

    print("rodar:", tube['angle'])
    rotateTo(tube['angle'])
    return tube['angle']

def backOriginalPosition(baseAngle):
    walkUntilDistance(2000, speed = -10, limit = 1000)
    rotateTo(180)
    rotateTo(-baseAngle)

    walkUntilColor(1)
    alinhar(1)

    rotateCm(30)
    rotateTo(180)
    walkUntilColor(1)
    alinhar(1)
    rotateCm(10)

def PegarTubo(count = 0, grab = False):
    # Rotaciona e acha o angulo onde o tubo se encontra
    tank.on_for_degrees(10, 10, 180)
    if(sc.value(0) == 4):
        grab = True
        
    baseAngle = alignWithTube(90, count = 1)
    if(baseAngle == "break"):
        return True

    # # Caminha até o tubo
    rotateCm(28)

    if(Comm.uf_value < 200):
        tank.on_for_degrees(10, 10, 90)
    else:
        tank.on_for_degrees(10, 10, -120)
        baseAngle += alignWithTube(40, test = False)
        tank.on_for_degrees(10, 10, 120)
    #caminha mais um pouco com a intenção de empurrar um pouco o tubo
    tank.on_for_degrees(10, 10, 45)

    for i in range (0,2):
        if(grabTube()):
            break

    if Comm.uf_value < 80 and grab:
        Mov_Garra_Sensor(1, 150)
        tank.on_for_degrees(10, 10, -360)
        rotateTo(180)
        rotateTo(-baseAngle)

        walkUntilColor(1)
        alinhar(1)

        controleCor = True

        return "pegou"
    else:
        tank.on_for_degrees(10, 10, -360)

        backOriginalPosition(baseAngle)
        print("Count do pegar Tubo:", count)
        if(count == 1):
            return True
        PegarTubo(count = count + 1)

    return True

def superior():
    if sc.value() == 1 or sc2.value() == 1:
        if ruido(1):
            print("Ruidopassou preto")
            alinhar(1)

            rotateCm(-25)
            rotateTo(80)

            walkUntilColor(0)
            alinhar(0)

            rotateCm(-41) #metade da primeira cor
            
            rotateTo(-90) # vira para a cor 

            walkUntilColor(1)
            alinhar(1) # entra na cor

            return True

    if sc.value() == 3 or sc2.value() == 3:
        if ruido(3):
            alinhar(3)

            rotateCm(-20)
            rotateTo(-85)

            walkUntilColor(0)
            alinhar(0)

            rotateCm(-41) #metade da primeira cor
            
            rotateTo(-90) # vira para a cor 

            walkUntilColor(1)
            alinhar(1) # entra na cor

            return True

    return False

def ruido(color):
    count = 0
    for i in range(0,5):
        print("ruido:", sc.value(), sc2.value())
        tank.on_for_degrees(10, 10, 10)
        if sc.value() == color or sc2.value() == color:
            count += 1

        tank.on_for_degrees(10, 10, -10)
        if sc.value() == color or sc2.value() == color:
            count += 1

    tank.on_for_degrees(10, 10, -10)

    if count > 8:
        return True

    return False

def queda(degrees = 180):
    if(sc.value() == 0 or sc2.value() == 0):
        rotateCm(2)
        if(sc.value() == 0 or sc2.value() == 0):
            tank.on_for_degrees(15, 15, -120)
            rotateTo(degrees)
            return True

    return False

def walkUntilQueda(speed = 10):
    count = 0
    while sc.value() != 1 and sc2.value() != 1:
        tank.on(speed, speed)
        if(sc.value() in [3]):
            tank.on_for_degrees(10, 10, -90)
            rotateTo(5)

        if(sc2.value() in [3]):
            tank.on_for_degrees(10, 10, -90)
            rotateTo(-5)
        pass
    tank.stop()

def Volta_Inicio():
    tank.stop()
    m1.run_to_rel_pos(position_sp=(-200),speed_sp=150,stop_action="brake")
    m2.run_to_rel_pos(position_sp=(-200),speed_sp=150,stop_action="brake")
    rotateTo(180)
    m1.run_forever(speed_sp=150)
    m2.run_forever(speed_sp=150)
    while (Comm.sc_value != 3) or (Comm.sc2_value != 3):
        m1.run_forever(speed_sp=150)
        m2.run_forever(speed_sp=150)
        if (us.value() > 100) or (us2.value() > 100) or (Comm.sc_value == 0) or (Comm.sc2_value == 0):
            Emergencia(120)        
    m1.run_to_rel_pos(position_sp=(-1000),speed_sp=150,stop_action="brake")
    m2.run_to_rel_pos(position_sp=(-1000),speed_sp=150,stop_action="brake")
    rotateTo(180)
    while (Comm.sc_value != 6) or (Comm.sc2_value != 6):
        m1.run_forever(speed_sp=-150)
        m2.run_forever(speed_sp=-150)
        if (us.value() > 100) or (us2.value() > 100) or (Comm.sc_value == 0) or (Comm.sc2_value == 0):
            Emergencia(120)
    time.sleep(1)
    
    tank.on_for_degrees(10, 10, 120)
    rotateTo(180)

def inicio():
    while True:
        tank.on(10, 10)

        if superior():
            break

def entra_aquatica():
    #quando sair do tubo estarei dentro da parte branca
    rotateCm(20)
    rotateTo(-90)

    walkUntilQueda()

    rotateCm(-15)
    rotateTo(90)
   
    walkUntilColor(3)
    alinhar(3)

    walkUntilColor(2)

    rotateCm(30)

    rotateTo(180)

    walkUntilColor(2)
    alinhar(2)

def proximaCor():
    rotateCm(5)
    rotateTo(180)

    walkUntilColor(6)
    alinhar(6)

    rotateCm(25)
    rotateTo(90)

    if not rotateCm(83): #False se acabar caindo
        rotateCm(-10)
        rotateTo(180)
        
        walkUntilQueda()
        alinhar(0)

        rotateCm(-41) #metade da primeira cor
        
        rotateTo(-90) # vira para a cor 

        walkUntilColor(1)
        alinhar(1) # entra na cor
    else:
        rotateTo(90)
        walkUntilColor(1)
        alinhar(1) # entra na cor

while True:
    inicio()

    i = 0
    while not controleCor:
        print(controleCor)
        print("dale", i)
        if i != 0:
            rotateCm(-20)
            rotateTo(-90)

            rotateCm(83)

            rotateTo(90)

            walkUntilColor(1)
            alinhar(1)

            rotateCm(5)
        
        if PegarTubo() == "pegou":
            break
        i += 1

    rotateCm(30)
    rotateTo(-90)

    walkUntilColor(0)
    alinhar(0)

    rotateCm(-20)

    rotateTo(90)

    walkUntilColor(3)
    alinhar(3)

    rotateCm(70)
    rotateTo(180)

    walkUntilColor(3)
    alinhar(3)

    print("well")

    if c_tubo(10):
        lego.parar()
        tank.stop()
        walkUntilColor(3, speed=-10)
        alinhar(2)

        walkUntilColor(1, speed=-10)
        alinhar(6)

        rotateCm(25)

        rotateTo(-90)

        walkUntilColor(0)
        alinhar(0)

        rotateCm(-40)

        rotateTo(-90)

        Mov_Garra_Sensor(0, 150)
        time.sleep(5)
    else:
        walkUntilColor(3, speed=-10)
        alinhar(2)

        walkUntilColor(1, speed=-10)
        alinhar(6)

        rotateCm(25)

        rotateTo(-90)

        walkUntilColor(0)
        alinhar(0)

        rotateCm(-40)

        rotateTo(-90)

        Mov_Garra_Sensor(0, 150)
        time.sleep(5)