def scan_gasoduto():
    tempo_inicio, tempos_pista, anterior_leitura = -1, [], 0
    tempo_dez, tempo_quinze, tempo_vinte = 0,0,0
    if alinhar(3) == 0:
        m1.run_forever(speed_sp=150)
        m2.run_forever(speed_sp=150)
        time.sleep(2)
        m1.stop(stop_action="brake")
        m2.stop(stop_action="brake")
        giraRobo(-90, 3)
        while True:
            m1.run_forever(speed_sp=150)
            m2.run_forever(speed_sp=150)
            if us.value() > 36 or us2.value() > 36:
                m1.stop_action("brake")
                m2.stop_action("brake")
                giraRobo(180)
                if len(tempos_pista) > 1:
                    tempos_pista.append(time.time())
            elif anterior_leitura == -1:
                tempos_pista.append(time.time()) 
                anterior_leitura = Comm.ir2_value
            elif (Comm.ir2_value - anterior_leitura) > 20: #Descobre um vao
                tempos_pista.append(time.time())
                anterior_leitura = Comm.ir2_value
                if tempo_inicio == 0:
                    tempo_inicio = time.time()
            elif (Comm.ir2_value - anterior_leitura) < 20: #Vao fechou
                tempos_pista.append(time.time())
                anterior_leitura = Comm.ir2_value
                if (time.time() - tempo_inicio) > 0:
                    print(str(time.time() - tempo_inicio))
                    time.sleep(15)
