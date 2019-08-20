def Intervalos(Intervalo):
    c, d = 0, 0 #crescer / decrescer
    for i in range(1, len(Intervalo),1):
        if (Intervalo[i] - Intervalo[i-1]) > 0:
            c += 1
        elif (Intervalo[i] - Intervalo[i-1]) < 0:
            d += 1
    return [c, d]


crecente = [10,11,12,13,14,15,16,17,13,14,15,16]
decrecente = [18,17,16,15,14,13,12,11,13,12,11,10]
osdois = [13,12,11,10,9,8,8,9,10,11,12,13]

print(Intervalos(crecente))
print(Intervalos(decrecente))
print(Intervalos(osdois))
