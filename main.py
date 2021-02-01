from Todim import Todim
import data_ingestion as di
import scrap


# PASSO 0 - Ingestão dos dados
(theta, colunas, pesos) = di.ingestTXT("matriz_decisao.txt")
(codigos, matriz) = di.ingestCSV(colunas)

# PASSO 1 - Carregar a matriz de decisão
matrizDecicao = Todim(matriz, pesos, codigos, theta, max=True)

# PASSO 2 - Normalizar a matriz de decisão de forma que em cada coluna o valor total seja igual a um.
matrizDecicao.normalizeMatrix()

# PASSO 3 - Normalizar ao peso dos criterios no intervalo [0,1]
matrizDecicao.normalizeWeights()

# PASSO 4 - Calcular o grau de dominância
matrizDecicao.getGrauDominio(verbose=True)

# PASSO 5 - Plotar um gráfico
matrizDecicao.plotBars()
