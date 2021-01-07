from Todim import Todim

# PASSO 1 - Carregar a matriz de decisão
matrizDecicao = Todim('matriz_decisao.txt')

# PASSO 2 - Normalizar a matriz de decisão de forma que em cada coluna o maior valor numérico seja igual a um.
matrizDecicao.normalizeMatrix()

# PASSO 3 - Normalizar ao peso dos criterios no intervalo [0,1]
matrizDecicao.normalizeWeights()

# PASSO 4 - Calcular o grau de dominância
matrizDecicao.getGrauDominio(verbose=True)

# PASSO 5 - Plotar um gráfico
# matrizDecicao.plotBars(['Alt 1', 'Alt 2', 'Alt 3'])
