import numpy as np
from numpy.lib.utils import deprecate
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate


class Todim:

    matrixD = None      # A matriz de decisão com as alternativas e criterios
    maximization = None  # Maximizar ou minimizar?
    weights = None      # Os pesos para cada criterio
    codes = None        # Os códigos de identificação das empresas
    wref = None         # Peso de referencia
    theta = None        # O valor de theta
    nAlt = None         # O numero de alternativas
    nCri = None         # O numero de criterios
    normMatrixD = None  # A matrizD normalizada
    phi = None          # Parcela de contribuição de um criterio
    delta = None        # Matriz nAlt x nAlt, cada endereço é composto pela dominancia de uma alternativa i sobre uma j
    cProximidade = None  # O coeficiente relativo de proximidade

    def __init__(self, *args, max=True):
        print("Inicializando as variáveis para o Método Todim")
        self.maximization = max
        if len(args) != 4:
            print("Não há parâmetros o suficiente.")
            raise ValueError

        self.matrixD = np.asarray(args[0])
        self.weights = np.asarray(args[1])
        self.codes = np.asarray(args[2])
        self.theta = args[3]

        tam = self.matrixD.shape
        [self.nAlt, self.nCri] = tam
        self.normMatrixD = np.zeros(tam, dtype=float)
        self.delta = np.zeros([self.nAlt, self.nAlt])
        self.rCloseness = np.zeros([self.nAlt, 1], dtype=float)

        """
        # unico parametro é o nome do arquivo por enquanto
        fileName = args[0]
        try:
            data = np.loadtxt(fileName, dtype=float)
        except IOError:
            print('Erro na leitura do arquivo de entrada!')
            raise IOError

        self.weights = data[0, :]
        self.theta = data[1, 0]
        self.matrixD = data[2:, :]

        # inicializar as variaveis
        tam = self.matrixD.shape
        [self.nAlt, self.nCri] = tam
        self.normMatrixD = np.zeros(tam, dtype=float)
        self.delta = np.zeros([self.nAlt, self.nAlt])
        self.rCloseness = np.zeros([self.nAlt, 1], dtype=float)

        self.printMatrix("Antes de tudo")
        """

    # normaliza a matriz
    def normalizeMatrix(self):
        m = self.matrixD.sum(axis=0)
        if self.maximization:
            for i in range(self.nAlt):
                for j in range(self.nCri):
                    self.normMatrixD[i, j] = self.matrixD[i, j] / m[j]
        else:
            for i in range(self.nAlt):
                for j in range(self.nCri):
                    self.normMatrixD[i, j] = (1/self.matrixD[i, j]) / (1/m[j])
        print('A matriz foi normalizada, o maior valor de cada coluna é igual a 1')
        self.matrixD = self.normMatrixD
        #self.printMatrix("depois de normalizar")

    # normaliza os pesos
    def normalizeWeights(self):
        if self.weights.sum() > 1.0000001 or self.weights.sum() < 0.9999999:
            self.weights = self.weights/self.weights.sum()
            print('Os pesos foram normalizados no intervalo [0,1]')
        # print(self.weights.sum())
        # peso de referencia
        self.wref = self.weights.max()
        # print(self.weights)

    # calcula o grau de dominio (matriz dominancia final)
    def getGrauDominio(self, verbose=False):
        self.getDelta()
        # self.printDelta()
        aux = self.delta.sum(axis=1)
        for i in range(self.nAlt):
            self.rCloseness[i] = (aux[i] - aux.min()) / (aux.max() - aux.min())
        if verbose:
            self.printResult()

    def getDelta(self):
        for i in range(self.nAlt):
            for j in range(self.nAlt):
                self.delta[i, j] = self.getSumPhi(i, j)
        # self.printDelta()

    def getSumPhi(self, i, j):
        # m = np.zeros(self.nCri)
        m = 0
        for c in range(self.nCri):
            m = m + self.getPhi(i, j, c)
            # self.printPhi()
        return m

    def getPhi(self, i, j, c):
        wcr = self.weights[c]/self.wref
        sumWRef = self.getSumWRef()
        dij = self.getDistance(i, j, c)
        comp = self.getComparison(i, j, c)
        if comp == 0:
            return 0
        elif comp > 0:
            return np.sqrt((wcr*abs(dij))/sumWRef)
        else:
            return np.sqrt((sumWRef*abs(dij))/wcr)/(-self.theta)

    def getSumWRef(self):
        sumWRef = 0
        for c in self.weights:
            sumWRef += c / self.wref
        return sumWRef

    def getDistance(self, alt_i, alt_j, crit):
        return (self.matrixD[alt_i, crit] - self.matrixD[alt_j, crit])

    # funcao modular para possibilitar outros tipos de comparações
    def getComparison(self, alt_i, alt_j, crit):
        return self.getDistance(alt_i, alt_j, crit)

    def printMatrix(self, s):
        # print(s)
        headers = ["col{}".format(i+1) for i in range(self.nCri)]
        table = tabulate(self.matrixD, headers,
                         tablefmt="fancy_grid", showindex=True)
        print(table)

    def printResult(self):
        # print("Não ordenado:")
        # print(self.rCloseness)
        # print("Ordenado:")
        # print(np.sort(self.rCloseness, axis=0)[::-1])
        pass

    def printDelta(self):
        for x in self.delta:
            print(x)
        print("\n\n")

    def plotBars(self, names=None, saveName=None):

        # une as matrizes com as abreviações dos nomes das debentures aos resultados obtidos respectivamente
        all_data = np.append(self.codes, self.rCloseness, 1)

        # ordena a matriz numpy de acordo com a segunda coluna(valores finais obtidos pelo Todim)
        ind = np.argsort(all_data[:, 1])
        all_data = all_data[ind]
        all_data = all_data[::-1]
        all_data = all_data[:20]
        print(all_data)

        # exibe uma grafico e barras
        sns.set_style("whitegrid")
        if self.codes is not None:
            # a = sns.barplot(all_data[:, 0], all_data[:, 1], palette="BuGn_d")
            a = sns.barplot(all_data[:, 1], all_data[:, 0], palette="BuGn_d")
        else:
            a = sns.barplot(None, self.rCloseness[:, 0], palette="BuGn_d")

        # a.set_ylabel("Closeness Coeficient")
        # a.set_xlabel('Alternatives')
        a.set_xlabel("Closeness Coeficient")
        a.set_ylabel('Alternatives')
        fig = a.get_figure()
        plt.show()

        if saveName is not None:
            fig.savefig(saveName+'.png')
