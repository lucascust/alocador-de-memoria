# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import algoritmo, aicSpider

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroi frame atual e cria o novo."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


#Classe da primeira janela
class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("Projeto AIC 3")

        #### Deixa Janela no centro
        larguraDaJanela = 300
        alturaDaJanela = 200

        larguraDaTela = master.winfo_screenwidth()
        alturaDaTela = master.winfo_screenheight()

        Xjanela = (larguraDaTela/2) - (larguraDaJanela/2)
        Yjanela = (alturaDaTela/2) - (alturaDaJanela/2)

        master.geometry("%dx%d+%d+%d" % (larguraDaJanela, alturaDaJanela, Xjanela,Yjanela))
        ############################

        #Variáveis para orientação automatizada da posição dos elementos na janela
        j = 0
        i = 0

        ##########Insersão do tamanho da memória
        textoTamMemoria = tk.Label(self, text="Tamanho da memória: ")
        textoTamMemoria.grid(column=i, row=j,padx=5)

        i += 1
        entradaTamMemoria = tk.Entry(self,width=10)
        entradaTamMemoria.grid(column=i, row=j,pady=25)
        j += 1

        ##############Opções de heurística
        i = 0
        textoOpcaoHeuristica = tk.Label(self, text="Heurística:")
        textoOpcaoHeuristica.grid(column=i, row=j)
        i += 1
        #Menu "bolinha"
        ##Varíavel que recebe opção escolhida
        selected = tk.IntVar()
        optionFirst = tk.Radiobutton(self,text='First Fit', value=1,variable = selected)
        optionFirst.grid(column=i, row=j)
        j+=1
        optionBest = tk.Radiobutton(self,text='Best Fit', value=2,variable = selected)
        optionBest.grid(column=i, row=j)
        j+=1
        optionWorst = tk.Radiobutton(self,text='Worst Fit', value=3,variable = selected)
        optionWorst.grid(column=i, row=j)
        j+=1

        ##Inicialização do algorítmo
        def botaoPressionado(PageTwo):
          global modo
          modo = selected.get()
          global tamMemoria
          tamMemoria = int(entradaTamMemoria.get())
          if (tamMemoria < 200):
            messagebox.showinfo('Erro!', 'O valor de memória deve ser maior que 200.')
            return
          if (tamMemoria > 1024):
            messagebox.showinfo('Erro!', 'O valor de memória deve ser menor que 1024.')
            return
          master.switch_frame(PageTwo)
        #Botão que inicia o algorítmo
        botaoInicio = tk.Button(self, text="Iniciar", command=lambda: botaoPressionado(PageTwo))
        botaoInicio.grid(column=i, row=j,pady=15)


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        master.title("Memória Tempo-Real")

        ### Deixa janela no centro
        larguraDaJanela = 1000
        alturaDaJanela = 300

        larguraDaTela = master.winfo_screenwidth()
        alturaDaTela = master.winfo_screenheight()

        Xjanela = (larguraDaTela/2) - (larguraDaJanela/2)
        Yjanela = (alturaDaTela/2) - (alturaDaJanela/2)

        master.geometry("%dx%d+%d+%d" % (larguraDaJanela, alturaDaJanela, Xjanela,Yjanela))
        ##########################

        #Função que gera uma cor aleatória
        def geraCor(posicaoProcesso,tamProcesso):
          codigoCor = '#'+str(abs(tamProcesso-posicaoProcesso))
          for i in range(len(codigoCor),7):
            codigoCor = codigoCor + "f"
          #Retorna um hexadecimal aleatório de seis digitos"#??????"
          return codigoCor

        #Criação do "canvas" -> Ambiente de desenho
        canvas = tk.Canvas(self, width=larguraDaJanela, height=100)

        # Cria as linhas que formam a memória
        def criaLinhas():
          lista = []
          i,x,y,y1 = 0,20,1,80
          while (x < (larguraDaJanela-20)):
            lista.append(canvas.create_line(x, y, x, y1, fill="#a0a0a0"))
            x += 1
          global numeroDeLinhasMemoria
          numeroDeLinhasMemoria = len(lista)
          return lista


        #### Legenda ########################
        if(modo == 1):
          textoHeuristica = tk.Label(self, text="First Fit",font = "Helvetica 16 bold")
          textoHeuristica.grid(column=1,row=0,padx=5)
        if(modo == 2):
          textoHeuristica = tk.Label(self, text="Best Fit",font = "Helvetica 16 bold")
          textoHeuristica.grid(column=1,row=0,padx=5)
        if(modo == 3):
          textoHeuristica = tk.Label(self, text="Worst Fit",font = "Helvetica 16 bold")
          textoHeuristica.grid(column=1,row=0,padx=5)


        textoLivre = tk.Label(self, text="(Cinza) Memória livre",font = "Helvetica 16 bold")
        textoLivre.grid(column=0, row=2,padx=5, pady=10)
        textoOcupada = tk.Label(self, text="(Azul) Memória Ocupada", font= "Helvetica 16 bold")
        textoOcupada.grid(column=2, row=2,padx=5, pady=10)
        ######################################

        ## Preenche a memória com o processo inserido
        ## Necessita do tamanho do processo, tamanho da memória e posição na memória
        def preencheMemoria(posicaoProcesso, tamProcesso):
          if(tamProcesso != 0):
            # Calucula quantas linhas devem ser preenchidas
            taxaDeLinhas = tamProcesso/tamMemoria
            numeroDeLinhas = taxaDeLinhas * len(listaDeLinhas)
            numeroDeLinhas = (int(numeroDeLinhas))+2
            # Descobre quanto vale cada linha desenhada
            pesoLinha = tamMemoria/len(listaDeLinhas)
            # Descobre em qual lugar da memória deve começar a pintar as linhas
            posicaoMemoria = posicaoProcesso/pesoLinha 
            posicaoMemoria = (int(posicaoMemoria))+2
            #Pinta do ponto range("X",y) até o ponto range(x,"Y")
            cor = geraCor(posicaoProcesso, tamProcesso)
            for i in range(posicaoMemoria,(posicaoMemoria+numeroDeLinhas)):
              canvas.itemconfig(i, fill=cor)
            if(posicaoProcesso == 0):
              for i in range(0,10):
                canvas.itemconfig(i, fill=cor)
            # print("Tamanho da Memoria: " + str(tamMemoria))
            # print("Tamanho do processo: " + str(tamProcesso))
            # print("Peso da Linha: " + str(pesoLinha))
            # print("Posição do processo: " + str(posicaoProcesso))
            # print("Numero de Linhas total: " + str(len(listaDeLinhas)))
            # print("Posição na memória: " + str(posicaoMemoria))
            # print("Numero de Linhas pra pintar: " + str(numeroDeLinhas)

        def limpaMemoria():
          for i in range(0,numeroDeLinhasMemoria):
            canvas.itemconfig(i, fill='#a0a0a0')
          

        ##### Botoes de Controle ######
        #Função Geral dos botoes
        def pressionado(listaDeEstados, botao):
          global momento
          if(botao == "proximo"):
            if (momento < len(listaDeEstados)-1):
              momento += 1
          if((botao == "anterior") and (momento != 0)):
            if (momento > 0):
              momento -= 1
          if(botao == "inicio"):
              momento = 0
          # Recebe lista do momento atual, com [Clock,[posiçãoInicial, tamanhoProcesso],[pos2,tam2]]
          estadoAtual = listaDeEstados[momento]
          # Atribui cada valor à sua respectiva variável
          ## Recebe e "printa" o Clock atual
          clock = estadoAtual[0]
          textoClock = tk.Label(self, text="Clock "+str(clock),font = "Helvetica 16 bold")
          textoClock.grid(column=2,row=0,padx=5)
          i = 1
          
          limpaMemoria()

          while (i <= len(estadoAtual)-1):
            posicaoProcesso = estadoAtual[i][0]
            tamProcesso = estadoAtual[i][1]
            # Preenche a memória com os dados informados
            preencheMemoria(posicaoProcesso, tamProcesso)
            i += 1


        #Função Executada quando é pressionado o Botao "Proximo"
        def pressionadoInicio(listaDeEstados):
            botao = "proximo"
            pressionado(listaDeEstados,botao)

        def pressionadoProximo(listaDeEstados):
            botao = "proximo"
            pressionado(listaDeEstados,botao)
        
        #Função Executada quando é pressionado o Botao "Anterior"
        def pressionadoAnterior(listaDeEstados):
            botao = "anterior"
            pressionado(listaDeEstados,botao)

        global listaDeLinhas
        listaDeLinhas = criaLinhas()

        #Cria lista com todos os momentos de entrada e saída de processos
        global matrizGeral
        matrizGeral = algoritmo.main(tamMemoria)
        listaDeEstados = matrizGeral[modo-1][0]
        listaDeEstados.insert(0,[0,[0,0]])

        # Momento (clock atual)
        global momento
        momento = 0

        # Declaração dos botões (função lambda necessária para passar parâmetros)
        botaoInicio = tk.Button(self, text="Inicio",command=lambda: pressionado(listaDeEstados,"inicio"))
        botaoProximo = tk.Button(self, text="Proximo",command=lambda: pressionado(listaDeEstados, "proximo"))
        botaoAnterior = tk.Button(self, text="Anterior",command=lambda: pressionado(listaDeEstados, "anterior"))
        botaoInicio.grid(column=1,row=3,pady=10)
        botaoProximo.grid(column=2,row=3,pady=10)
        botaoAnterior.grid(column=0,row=3,pady=10)
        # Função do botao que chama o matplot
        def pressionadoGrafico(PageThree):
            # Opção 1: Chamar janela tkinter que recebe imagem do matplot
            #master.switch_frame(PageThree)
            # Opção 2: Chamar matplot direto
            self.master.destroy()
            aicSpider.main(matrizGeral)
        botaoGraficos = tk.Button(self, text="Ir Para Gráficos",command=lambda: pressionadoGrafico(PageThree))
        botaoGraficos.grid(column=1,row=4,pady=5)
        #Posição do Canvas
        canvas.grid(columnspan=3,row=1)


#Tentativa de fazer uma terceira janela TkInter
class PageThree(tk.Frame):

      def __init__(self, master):
        tk.Frame.__init__(self, master)

        master.title("Gráfico de resultados")

        ### Deixa janela no centro
        larguraDaJanela = 300
        alturaDaJanela = 300

        larguraDaTela = master.winfo_screenwidth()
        alturaDaTela = master.winfo_screenheight()

        Xjanela = (larguraDaTela/2) - (larguraDaJanela/2)
        Yjanela = (alturaDaTela/2) - (alturaDaJanela/2)

        master.geometry("%dx%d+%d+%d" % (larguraDaJanela, alturaDaJanela, Xjanela,Yjanela))
        ##########################
        aicSpider.main()
        #img = aicSpider.main()
        label = tk.Label(self, text="This is page 2")
        label.grid(pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()





        # Menu superior
        # menu = Menu(self)
        # new_item = Menu(menu)
        # new_item.add_command(label='New')
        # new_item.add_separator()
        # new_item.add_command(label='Edit')
        # menu.add_cascade(label='File', menu=new_item)
        # self.config(menu=menu)

 