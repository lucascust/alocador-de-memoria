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
import timeit
import funcoes as f

def main(tamMemoria):
    listaSaida = []
    modos=["first","best","worst"]
    for a in modos:
        modo=a
        #INICIALIZAÇÃO: Criação das estruturas necessárias
        processos = f.interpreta("entrada.txt")
        f.listaDeTamanhos(processos)
        dicionarioDeEntrada = f.dicionarioDeEntrada(processos)
        dicionarioDeSaida = f.dicionarioDeSaida(processos)
        dicionarioDeProcessos = {}
        clock = 0

        """print("\nDicionário de Entradas:\n")
        print(dicionarioDeEntrada, end='\n\n')
        print("Dicionário de Saídas:\n")
        print(dicionarioDeSaida,end='\n\n')"""

        tentativasFalhadas = 0
        tempoEspera = [0] * len(processos) #Inicializa vetor dos tempos de espera
        tempoAlocacao = []
        entradaParteGrafica =[]

        del processos
        ##################################################
        #Início algoritmo: Cada loop é um ciclo
        while (dicionarioDeSaida):
            dicanterior = str(dicionarioDeProcessos) #Utilizado no print de quando muda alguma coisa no dicionárioDeProcessos

            #Inserção de processo
            if (clock in dicionarioDeEntrada):
                while (dicionarioDeEntrada[clock]):
                    processo = dicionarioDeEntrada[clock].pop() #Remove e salva ultimo elemento da lista
                    
                    tinicial = timeit.default_timer() #Usado para avaliar o tempo de inserção dos processos
                    dicionarioDeProcessos, inseriu = f.alocarMemoria(processo,tamMemoria,dicionarioDeProcessos,modo)
                    tfinal= timeit.default_timer()

                    tempoAlocacao = f.tempoMedioDeAlocacaoDeProcessos(tempoAlocacao,inseriu,tfinal,tinicial) 
                    tentativasFalhadas = f.tentativasFalhas(inseriu,tentativasFalhadas) #Atualiza o número de falhas do algoritmo
                    tempoEspera = f.tempoMedioDeEsperaDeProcessos(inseriu,tempoEspera,processo)
                    
                    if (inseriu==False):
                        if (dicionarioDeEntrada.get(clock+1, False)):
                            dicionarioDeEntrada[clock+1].append(processo)
                        else:
                            dicionarioDeEntrada[clock+1]=[processo]
                        for i in dicionarioDeSaida:
                            if processo in dicionarioDeSaida[i]:
                                tempoDeSaida = i
                        if (dicionarioDeSaida.get(tempoDeSaida+1, False)):
                            dicionarioDeSaida[tempoDeSaida+1].append(processo)
                        else:
                            dicionarioDeSaida[tempoDeSaida+1]=[processo]
                        
                        dicionarioDeSaida[tempoDeSaida].remove(processo)
                        
            #Remoção de processo
            if (clock in dicionarioDeSaida):
                while (dicionarioDeSaida[clock]):
                    processo = dicionarioDeSaida[clock].pop() #Remove e salva ultimo elemento da lista
                    dicionarioDeProcessos = f.desalocaProcesso(processo,dicionarioDeProcessos)
                del dicionarioDeSaida[clock]


            if (dicanterior!=str(dicionarioDeProcessos)): #Só printa quando há uma alteração no dicionario
                #print(clock , dicionarioDeProcessos,end="\n\n")
                entradaParteGrafica = f.geraEntradaDaParteGrafica(entradaParteGrafica,clock,dicionarioDeProcessos) #Gera os dados necessários para parte gráfica
            clock+=1
        #Chamadas de funções para exibir os resultados finais
        clock_final = entradaParteGrafica[-1]
        del entradaParteGrafica[-1]

        nivelFragmentacaoMemoria = round(f.media(f.calculaFragmentacaoMemoria(entradaParteGrafica,clock_final,tamMemoria)),3) #Quantos buracos existem na memória por ciclo de CLOCK
        mediaTempoEspera = round(f.media(tempoEspera),3)
        tempoAlocacao = round(f.media(tempoAlocacao)*1000000,3) #Tempo em μs
        #print("Nº de tentativas falhas: " + str(tentativasFalhadas) + " inserções falhas")
        #print("Tempo médio de espera dos processos: " + str(mediaTempoEspera) + " períodos de clock")
        #print("Tempo médio para alocação de processos: " + str(tempoAlocacao) + " segundos")
        #print("média de buracos por ciclo de CLOCK: " +str(nivelFragmentacaoMemoria))
        entradaParteGrafica.append(clock_final) #adicionado para mostrar quando a memória fica vazia
        listaSaida.append([entradaParteGrafica,mediaTempoEspera,tentativasFalhadas,nivelFragmentacaoMemoria,tempoAlocacao])

    return listaSaida
