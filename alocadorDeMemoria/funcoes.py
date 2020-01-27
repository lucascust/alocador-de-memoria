#encoding=utf-8
#DEFINIÇÃO DO PADRÃO DE ESCRITA
    #COMENTÁRIOS
        #1º Modo de escrita dos comentários livre, ´~^-_+=, etc, permitidos
            #ex: meu nome é, variável de saída
    #FUNÇÕES
        #2º Nomes das funções SEM ´~^-_+=, etc. E pode usar "De"
        #3º Comentários no início das funções explicando o que fazem
        #4º Comentários no final das funções explicando o que retornam
            #ex: meuNomeE, variavelDeSaida
    #VARIÁVEIS
        #5º Variáveis iniciadas em mínuscula, SEM ´~^-_+= etc, SEM "De", se tiver mais de uma palavra, esta, deve ser iniciada em maíuscula
            #ex: meuNomeE, variavelSaida

#Extrai valores do txt para criar as estruturas
def interpreta(arquivo):
    arq = open(arquivo,"r")
    processos = arq.readlines()
    for i in range(len(processos)):
        processos[i] = processos[i].strip()
        processos[i] = processos[i].split(" ")
    for i in range(len(processos)):
        for j in range(len(processos[i])):
            processos[i][j] = int(processos[i][j]) 
    #lista de processos = [[int tempo de chegada, int tempo de execução,int tamanho],...]
    return processos

#Extrai valores da lista de processos para criar uma lista com os tamanhos de cada processo
def listaDeTamanhos(processos):
    global tamanhos
    tamanhos = []
    for i in processos:
        tamanhos.append(i[2])
    #lista de tamanho dos processos = [tamanho,...]

#Extrai valores da lista de processos para criar um dicionário com os tempos de entrada de cada processo
def dicionarioDeEntrada(processos):
    temposEntrada ={}
    processoAtual=0
    for i in processos:
        if (i[0] in temposEntrada):#processos[2] é tempo de chegada
            temposEntrada[i[0]].append(processoAtual)
        else:
            temposEntrada[i[0]]= [processoAtual]
        processoAtual+=1
    #dicionário com os tempos de entrada dos processos = {ciclo de entrada:nº do processo,...}
    return temposEntrada

#Extrai valores da lista de processos para criar um dicionário com os tempos de saída de cada processo
def dicionarioDeSaida(processos):
    temposSaida ={}
    processoAtual=0
    for i in processos:
        if ((i[1]+i[0]) in temposSaida):
            temposSaida[i[1]+i[0]].append(processoAtual)
        else:
            temposSaida[i[1]+i[0]]= [processoAtual]
        processoAtual+=1
    #dicionário com os tempos de saída dos processos = {ciclo de Saida:nº do processo,...}
    return temposSaida

#Desaloca processo do dicionário de processos
def desalocaProcesso(processo,dicionarioDeProcessos):
    anterior = dicionarioDeProcessos[processo][2]
    posterior = dicionarioDeProcessos[processo][3]
    try:
        dicionarioDeProcessos[anterior][3]=posterior
    except:
        pass
    try:
        dicionarioDeProcessos[posterior][2]=anterior
    except:
        pass
    del dicionarioDeProcessos[processo]
    #Retorna dicionário atualizado
    return dicionarioDeProcessos

#Varre a memória de acordo com a eurística determinada, retornando qual será o processo anterior à nova inserção
def varreMemoria(dicionarioDeProcessos,tamanhoProcesso,modo,tamMemoria):

    #Caso o dicionário esteja vazio
    if not (dicionarioDeProcessos):
        return "I","F"

    #Inicialização quando tem pelo menos um processo na memória
    for i in dicionarioDeProcessos:
        if("I" in dicionarioDeProcessos[i]):
            processoAtual = i
            if(tamanhoProcesso <= dicionarioDeProcessos[i][0]):
                menorDistancia = dicionarioDeProcessos[i][0]
                maiorDistancia = dicionarioDeProcessos[i][0]
                maiorProcesso = "I"
                menorProcesso = "I"
                processoPosterior = i
                if(modo == "first"):
                    return "I",processoAtual
            else:
                menorDistancia = float('inf')
                maiorDistancia = 0
                
    processoSeguinte=dicionarioDeProcessos[processoAtual][3]

    while(True):
        if(processoSeguinte == "F"):
            distancia = tamMemoria-dicionarioDeProcessos[processoAtual][1]
        else:
            distancia = dicionarioDeProcessos[processoSeguinte][0]-dicionarioDeProcessos[processoAtual][1]
        if ((modo == "first") and (tamanhoProcesso<=distancia)):
            return processoAtual,dicionarioDeProcessos[processoAtual][3]
        if ((distancia<menorDistancia) and (tamanhoProcesso<=distancia)):
            menorDistancia = distancia
            menorProcesso = processoAtual
        if ((distancia>maiorDistancia) and (tamanhoProcesso<=distancia)):
            maiorDistancia = distancia
            maiorProcesso = processoAtual
        processoAtual=processoSeguinte
        if(processoAtual=="F"):
            break
        else:
            processoSeguinte= dicionarioDeProcessos[processoSeguinte][3] 
    if(maiorDistancia!=0):
        if(modo=="worst"):  
                try:
                    return maiorProcesso,dicionarioDeProcessos[maiorProcesso][3]
                except:
                    return maiorProcesso, processoPosterior
        elif(modo=="best"):
                try:
                    return menorProcesso,dicionarioDeProcessos[menorProcesso][3]
                except:
                    return menorProcesso, processoPosterior
    else:
        #Retorna situação onde não cabe o processo
        return -1,-1

#Aloca processo no dicionário de processos
def alocarMemoria(processo,tamMemoria,dicionarioDeProcessos,modo):
    processoAnterior,processoPosterior = varreMemoria(dicionarioDeProcessos,tamanhos[processo],modo,tamMemoria)
    if(processoAnterior == -1):

        return dicionarioDeProcessos, False
    padrao = True
    if (processoPosterior != "F"):
        dicionarioDeProcessos[processoPosterior][2]=processo
    else:
        padrao=False
        try:
            posicao = dicionarioDeProcessos[processoAnterior][1]
        except:
            posicao = 0
    if (processoAnterior != "I"):
        dicionarioDeProcessos[processoAnterior][3]=processo
    else:
        padrao=False
        posicao = 0
    if(padrao==True):
        posicao = dicionarioDeProcessos[processoAnterior][1]

    dicionarioDeProcessos[processo]=[posicao,posicao+tamanhos[processo],processoAnterior,processoPosterior]
       
    return dicionarioDeProcessos, True

#Função que incrementa o número de tentativas falhas a cada vez que não conseguir inserir um processo
def tentativasFalhas(inseriu,tentativasFalhadas):
    if (inseriu==False):
        tentativasFalhadas+=1
        return tentativasFalhadas
    return tentativasFalhadas

#Função que incrementa o tempo de espera de cada processo, tem uma lista onde cada elemento representa o tempo que aquele processo aguardou
def tempoMedioDeEsperaDeProcessos(inseriu,tempoEspera,processo):
    if (inseriu==False):
        tempoEspera[processo]+=1
        return tempoEspera
    return tempoEspera

#Cálcula a média do tempo de espera para inserção dos processos na memória, e a média dos tempos médios de alocação
def media(lista):
    somatorio=0
    for i in lista:
        somatorio+=i
    media=somatorio/(len(lista))
    return media

#Função que adiciona o tempo de inserção dos processos na memória em segundos, à uma lista
def tempoMedioDeAlocacaoDeProcessos(tempoAlocacao,inseriu,tfinal,tinicial):
    if (inseriu!=False):
        time = (tfinal - tinicial)
        tempoAlocacao.append(time)
        return tempoAlocacao
    return tempoAlocacao

#Retorna os dados necessários para parte gráfica do algoritmo
def geraEntradaDaParteGrafica(entradaParteGrafica,clock,dicionarioDeProcessos):
    def funcao(var):
        return var[0]    
    indiceClock = [clock] #Índice da lista "entradaParteGrafica" que também é uma lista
    processos = list(dicionarioDeProcessos.values())
    processos.sort(key=funcao) #Ordena matriz pelo 1º indície
    for i in processos:
        indiceClock.append([i[0],i[1]-i[0]]) #append em indiceclock
    entradaParteGrafica.append(indiceClock) 
    return entradaParteGrafica

#Retorna uma lista com o número de buracos por ciclo de CLOCK na memória
def calculaFragmentacaoMemoria(entradaParteGrafica,clock_final,tamMemoria):
    buracosPorClock=[]

    #Período inicial que tinha 1 buraco, antes da primeira inserção de processo
    for i in range(entradaParteGrafica[0][0]): #Adiciona os buracos do inicio
        buracosPorClock.append(1)

    buracosFinal=0 #Período final do algoritmo

    if(entradaParteGrafica[-1][1][0]>0):
        buracosFinal+=1
    if((entradaParteGrafica[-1][-1][0]+entradaParteGrafica[-1][-1][1])<tamMemoria):
        buracosFinal+=1
    if(len(entradaParteGrafica[-1])>2):       
        for i in range(len(entradaParteGrafica[-1])-2):
            if((entradaParteGrafica[-1][i+2][0]-(entradaParteGrafica[-1][i+1][1]+entradaParteGrafica[-1][i+1][0]))>0):
                buracosFinal+=1
    for i in range(clock_final[0]-entradaParteGrafica[-1][0]): 
        buracosPorClock.append(buracosFinal)

    for i in range(len(entradaParteGrafica)-1): #Período intermediário do algoritmo
        buracosMeio = 0
        if(len(entradaParteGrafica[i])==1):#Caso não tenha processos
            buracosMeio+=1
        else: #tem um processo ou mais
            if(entradaParteGrafica[i][1][0]>0):
                buracosMeio+=1
            if((entradaParteGrafica[i][-1][0]+entradaParteGrafica[i][-1][1])<tamMemoria):
                buracosMeio+=1
            if(len(entradaParteGrafica[i])>2):
                for j in range(len(entradaParteGrafica[i])-2):###
                    if((entradaParteGrafica[i][j+2][0]-(entradaParteGrafica[i][j+1][1]+entradaParteGrafica[i][j+1][0]))>0):
                        buracosMeio+=1

        for j in range(entradaParteGrafica[i+1][0]-entradaParteGrafica[i][0]):
            buracosPorClock.append(buracosMeio)
    return buracosPorClock