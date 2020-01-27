# Alocador de memória virtual interativo
[Lucas Custódio](https://github.com/lucascust) e [Frederico Bender](https://github.com/FredericoBender)

Software desenvolvido em Python com representação visual de uma memória primária sendo alocada por processos através de três famigeradas heurísticas: First Fit, Best Fit e Worst Fit. Além disso, o algoritmo apresenta um gráfico Spider com indicadores de performance para comparação do desempenho das heurísticas após a simulação.

**Tecnologias e estruturas usadas: Dicionários Python, matplotlib, listas encadeadas.**

### Entendendo as heuristicas para o alocamento de um processo na memória
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

### Funcionamento do Algoritmo

O gerenciador de memória será administrado pela manipulação de dicionários em python. O algoritmo recebe um texto com diversos processos, com seus respectivos momentos de entrada, tempo que permanecerá na memória e seu tamanho. O tempo utilizado é em ciclos de relógio (clock). Esses dados são    transformados em estruturas: a representação da mememória física, e os momentos de entrada e saída dos processos são mantidos em dicionários.

#### Formato da entrada do código
A entrada é dada por um arquivo .txt da seguinte forma:
```
...
017 39 073
043 45 172
013 28 073
...
```
Cada linha é um processo, o pimeiro valor é o ciclo que o processo entrará na memória, o segundo valor representa o tempo de execução do processo e por fim, o ultimo valor é o tamanho do processo.

#### Geração das estruturas iniciais

Após receber documento de entrada, o algoritmo gera três estruturas: 
- Dicionário de entrada: Possui todos os momentos que haverá entrada de processos na memória, para cada momento todos os processos que entrarão (caso entrem procesos simultâneamente naquele ciclo) serão armazenados em uma lista.
- Dicionário de saída: Através dos dados recebidos, estima-se o momento de saída dos processos e cria um dicionário similar ao de entras, porém, os tempos representam o momento de saída.
- Lista de tamanhos: Uma lista ordenada com os tamanhos do processo

Os dicionários de entrada e saída possuem o tempo de clock como ***chave***, e como ***valor*** da chave, a lista dos processos a serem inseridos/removidos da memória. A imagem abaixo ilustra essa estrutura.

<h4 align="center">
    <img alt="inoutdic" src="https://res.cloudinary.com/df8snvgem/image/upload/c_scale,h_500/v1579974872/alocador-de-memoria/dicionarios-iniciais_qx7bsm.jpg" />
</h4>

