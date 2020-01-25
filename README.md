# Alocador de memória virtual interativo
[Lucas Custódio](https://github.com/lucascust) e [Frederico Bender](https://github.com/FredericoBender)

Software desenvolvido em Python com representação visual de uma memória primária sendo alocada por processos através de três famigeradas heurísticas: First Fit, Best Fit e Worst Fit. Além disso, o algoritmo apresenta um gráfico Spider com indicadores de performance para comparação do desempenho das heurísticas após a simulação.

**Tecnologias e estruturas usadas: Dicionários Python, matplotlib, listas encadeadas.**

### Entendendo as heuristicas para o alocamento de um processo na memória
Para ilustrar as heurísticas, consideremos uma ilustração de uma memória com alguns processos alocados e também alguns espaços livres. No exemplo o Sistema Operacional precisa alocar um processo de 5kb e existem diferentes possibilidades de espaços disponíveis. Abaixo é apresentado como cada metodologia alocaria o processo:

- First Fit: O processo é alocado no primeiro espaço disponível encontrado pelas comparações do algoritmo.
![firstfit](https://res.cloudinary.com/df8snvgem/image/upload/v1579971567/alocador-de-memoria/first-fit_rvhcgv.png)

- Best Fit: O algoritmo busca encontrar o espaço na memória cujo tamanho é o mais próximo do tamanho do processo, em outras palavras, o menor espaço disponível que seja compatível.
![bestfit](https://res.cloudinary.com/df8snvgem/image/upload/v1579971567/alocador-de-memoria/best-fit_vjusqk.png)

- Worst Fit: A alocação do processo é feita no maior espaço disponível na memória, ou seja, no espaço com a maior diferença de tamanho em relação ao 
processo.
![worstfit](https://res.cloudinary.com/df8snvgem/image/upload/v1579971567/alocador-de-memoria/worst-fit_cwoj7r.png)


### Funcionamento do Algoritmo


