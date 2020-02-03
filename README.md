# Alocador de Memória Interativo

[Lucas Custódio](https://github.com/lucascust) e [Frederico Bender](https://github.com/FredericoBender)

Software desenvolvido em Python com representação visual de uma memória primária sendo alocada por processos através de três famigeradas heurísticas: First Fit, Best Fit e Worst Fit. Além disso, o algoritmo apresenta um gráfico Spider com indicadores de performance para comparação do desempenho das heurísticas após a simulação.

**Tecnologias e estruturas usadas: Dicionários Python, matplotlib, tkinter, listas encadeadas.**

## Resumo do Projeto
---
O software apresenta uma janela com inputs para inserir o tamanho total da memoria e a heurístida desejada para visualização. Em seguida recebe um documento de texto com todos os processos que entrarão na memória, informando o tamanho e quanto tempo permanecerá. Com os dados, executa-se o algoritmo de alocação para as três heurísticas. Uma janela interativa permite o usuário a acompanhar o passo a passo da metodologia escolhida e por fim mostra um gráfico de desempenho de cada heurística para comparações.

## Entendendo as heuristicas para o alocamento de um processo na memória
---
Para ilustrar as heurísticas, consideremos uma ilustração de uma memória com alguns processos alocados e também alguns espaços livres. No exemplo o Sistema Operacional precisa alocar um processo de 5kb e existem diferentes possibilidades de espaços disponíveis. Abaixo é apresentado como cada metodologia alocaria o processo:

- First Fit: O processo é alocado no primeiro espaço disponível encontrado pelas comparações do algoritmo.
<h4 align="center">
    <img alt="First-fit" src="https://res.cloudinary.com/df8snvgem/image/upload/c_scale,h_300/v1579971567/alocador-de-memoria/first-fit_rvhcgv.png" />
</h4>


- Best Fit: O algoritmo busca encontrar o espaço na memória cujo tamanho é o mais próximo do tamanho do processo, em outras palavras, o menor espaço disponível que seja compatível.
<h4 align="center">
    <img alt="best-fit" src="https://res.cloudinary.com/df8snvgem/image/upload/c_scale,h_300/v1579971567/alocador-de-memoria/best-fit_vjusqk.png" />
</h4>

- Worst Fit: A alocação do processo é feita no maior espaço disponível na memória, ou seja, no espaço com a maior diferença de tamanho em relação ao 
processo.
<h4 align="center">
    <img alt="worst-fit" src="https://res.cloudinary.com/df8snvgem/image/upload/c_scale,h_300/v1579971567/alocador-de-memoria/worst-fit_cwoj7r.png" />
</h4>

## Funcionamento do Algoritmo
---
O gerenciador de memória será administrado pela manipulação de dicionários em python. O algoritmo recebe um texto com diversos processos, com seus respectivos momentos de entrada, tempo que permanecerá na memória e seu tamanho. O tempo utilizado é em ciclos de relógio (clock). Esses dados são    transformados em estruturas: a representação da mememória física, e os momentos de entrada e saída dos processos são mantidos em dicionários.

### Formato da entrada do código
---
A entrada é dada por um arquivo .txt da seguinte forma:
```
...
017 39 073
043 45 172
013 28 073
...
```
Cada linha é um processo, o pimeiro valor é o ciclo que o processo entrará na memória, o segundo valor representa o tempo de execução do processo e por fim, o ultimo valor é o tamanho do processo.

### Geração das estruturas iniciais
---
Após receber documento de entrada, o algoritmo gera três estruturas: 
- Dicionário de entrada: Possui todos os momentos que haverá entrada de processos na memória, para cada momento todos os processos que entrarão (caso entrem procesos simultâneamente naquele ciclo) serão armazenados em uma lista.
- Dicionário de saída: Através dos dados recebidos, estima-se o momento de saída dos processos e cria um dicionário similar ao de entras, porém, os tempos representam o momento de saída.
- Lista de tamanhos: Uma lista ordenada com os tamanhos do processo

Os dicionários de entrada e saída possuem o tempo de clock como ***chave***, e como ***valor*** da chave, a lista dos processos a serem inseridos/removidos da memória. A imagem abaixo ilustra essa estrutura.

<h4 align="center">
    <img alt="inoutdic" src="https://res.cloudinary.com/df8snvgem/image/upload/c_scale,h_300/v1579974872/alocador-de-memoria/dicionarios-iniciais_qx7bsm.jpg" />
</h4>

### Memória principal
---
A memória é “representada” por um terceiro dicionário, onde as chaves serão os processos que estão atualmente na memória. O valor dessas chaves será uma lista de tamanho 4, seus significados são expressados na figura abaixo.

<h4 align="center">
    <img alt="inoutdic" src="https://res.cloudinary.com/df8snvgem/image/upload/v1580121563/alocador-de-memoria/memoria-principal_kvhyar.png" />
</h4>

A lista-valor armazena em suas duas primeiras posições, os valores **X** e **Y**, que são o as posições que processo fica armazenado, ou seja, leia-se *“O processo está alocado na memória da posição X até Y”*. Considerando que não haverá um armazenamento para os espaços vazios, as posições dos processos são usadas para calcular os espaços entre um processo e outro, retornando os espaços. Saber qual o próximo processo na memória para realizar o cálculo é o problema solucionado pelos próximos dois índices da lista. Os valores **A** e **P** representam respectivamente o processo **anterior** e **posterior** em relação ao processo atual, caracterizando uma estrutura **DUPLAMENTE ENCADEADA**. Vislumbrando a memória como uma “torre” e que o algoritmo irá varrer-lá de baixo para cima, a ordem dos processos é dada pela posição relativa na memória, em outras palavras, quanto mais “embaixo” o processo tiver, menor será sua posição. Exemplificando essa ordenação, a imagem abaixo mostra uma memória com processos alocados, e com números mostrando suas respectivas posições. Além disso, é ilustrado o encadeamento dos processos através dos dicionários.

<h4 align="center">
    <img alt="inoutdic" src="https://res.cloudinary.com/df8snvgem/image/upload/v1580121558/alocador-de-memoria/processpositioning_kpwdnu.png" />
</h4>

Os valores de encadeamento **A** e **P**  são utilizados para saber entre quais processos (em qual epaço) na memória o cálculo do tamanho dos espaços deve ser feito. Cada vez que um elemento for inserido ou removido, esses valores devem ser atualizados para continuar correspondendo a lógica. Sendo capaz de calcular o tamanho dos espaços na memória Através das estruturas citadas, é possível calcular o tamanho dos espaços na memória, com isso, basta aplicar as heurísticas propostas para gerenciar a memória. 

### Interface Gráfica
---
Utilizando o módulo Tkinter, É gerado a representação da memória vazia (cinza) e botões para escolha do ciclo atual. Ao avançar os ciclos, cores em tom de azul preenchem parte da memória para representar os diferentes processos. 

<!-- imagem -->

A implementação gráfica dessa memória se dá por uma série de linhas verticais lado a lado. Inicialmente todas cinzas, são trocadas de cor a medida que os processos são alocados na memória. O tamanho do processo a ser preenchido é calculado como proporção da memória total em relação ao número de linhas, substituindo o número de linhas correspondentes. Leva-se em conta tembém a posição, estimada igualmente com a proproção tamanho-linhas.

### Resultados - Spider Graph com Matplotlib 
---
A fim de análise do desempenho das heurísticas, é utilizado métricas de performance que são calculadas ao longo da execução do algoritmo. O funcionamento e o objetivo das métricas são:

- **Tempo Médio de Espera de Processos (TMEP)**:
Informa quantos ciclos em média um processo aguarda para ser inserido na memória. A partir do momento que um processo não conseguir entrar na memória, um contador, que será sempre inicializado em 0, será incrementado em 1. Quando o processo for inserido com sucesso a memória, esse contador, será adicionado a uma lista, que vai conter o tempo de espera que cada processo teve até sua inserção, no fim, basta fazer a média dos valores na lista.

- **Tempo Médio para Alocação de Processos (TMAP)**:
Assim que o Tempo Médio de Espera do processo atual for inserido a lista, será utilizada uma função simples do Python para medir o tempo até o momento em que o algoritmo encontre o local de inserção do elemento. Apesar de fazer uma análise temporal da execução de um algoritmo ser algo instável para que se tenha uma conclusão confiável, essa informação pode ajudar a ilustrar a diferença de performance das heurísticas.

- **Número de Tentativas Falhas (NTF)**:
Este indicador mostra quantas vezes um processo não pode ser alocado. Cada vez que um processo tentar alocar um bloco da memória, e não existir espaço disponível para ela, um contador é incrementado.

- **Nível de Fragmentação da Memória (NFM)**:
Mostra o número de espaços a memória, pois um maior número de "buracos" implica em inutilização de espaços na memória podendo impedir processos de ser alocados mesmo quando há espaço disponível na memória. A cada ciclo de CLOCK, vamos utilizar um contador, para verificar quantos buracos de espaços livres existem na memória e adicionar em uma lista, para calcular a média de buracos existentes por ciclo de CLOCK no final. 

**OBS**: Durante esta medida, o tempo transcorrido pelo medidor de tempo do dado: Tempo Médio para Alocação de Processos, deverá ser pausado.

### Apresentação das métricas
---
Para apresentar as métricas, é necessário normalizar os dados, pois a magnitude dos valores é discrepante. Logo, os valores são transformados em proporções, baseadas no resultado de maior valor. O programa gera um gráfico em teia com o resultado dos cálculos de cada métrica e de forma sobreposta, para cada heurística, como apresentado na figura a seguir:

<!-- /FIGURA --> 




