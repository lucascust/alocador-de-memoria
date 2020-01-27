# Gera processos aleatoriamente para utilização no algoritmo

# nprocessos: Número de processos a ser gerado
# Tamanho do processo: 1 à 500
# Tempo de execução: 20 à 50
# Momento (clock) de entrada do processo: 20 à 200


import random

arq1 = open("arq1.txt", "w")
arq2 = open("arq2.txt", "w")
nprocessos = 55

for i in range(0, nprocessos*2, 1):
    tam = random.randint(1,500)
    tempo_exec = random.randint(20, 50)
    tempo_cheg = random.randint(50, 200) # Pode mudar
    if (i < nprocessos):
        arq1.write(str(tam) + " " + str(tempo_exec) + " " + str(tempo_cheg) + "\n")
    else:
        arq2.write(str(tam) + " " + str(tempo_exec) + " " + str(tempo_cheg) + "\n")
arq1.close()
arq2.close()
