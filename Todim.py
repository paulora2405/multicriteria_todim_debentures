import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class Todim:

    matrixD = None      # A matriz de decisão com as alternativas e criterios
    weights = None      # Os pesos para cada criterio
    wref = None
    theta = None        # O valor de theta
    nAlt = None         # O numero de alternativas
    nCri = None         # O numero de criterios
    normMatrixD = None  # A matrizD normalizada
    phi = None
    delta = None
    cProximidade = None   # O coeficiente relativo de proximidade

    def __init__(self, *args):
        nargs = len(args)

        # unico parametro é o nome do arquivo por enquanto
        fileName = args[0]
        try:
            data = np.loadtxt(fileName, dtype=float)
        except IOError:
            print('ERROR: erro na leitura do arquivo de entrada!')
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

    # normaliza a matriz
    def normalizeMatrix(self):
        m = self.matrixD.sum(axis=0)
        for i in range(self.nAlt):
            for j in range(self.nCri):
                self.normMatrixD[i, j] = self.matrixD[i, j] / m[j]
        print('A matriz foi normalizada, o maior valor de cada coluna é igual a 1')
        self.matrixD = self.normMatrixD
        # print(self.matrixD)

    # normaliza os pesos
    def normalizeWeights(self):
        if self.weights.sum() > 1.001 or self.weights.sum() < 0.9999:
            self.weights = self.weights/self.weights.sum()
            print('Os pesos foram normalizados no intervalo [0,1]')
        # print(self.weights.sum())
        # peso de referencia
        self.wref = self.weights.max()

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
        #m = np.zeros(self.nCri)
        m = 0
        for c in range(self.nCri):
            m = m + self.getPhi(i, j, c)
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

    def printResult(self):
        print(self.rCloseness)
        print(np.sort(self.rCloseness, axis=0)[::-1])

    def printDelta(self):
        for x in self.delta:
            print(x)
        print("\n\n")

    def plotBars(self, names=None, saveName=None):
        sns.set_style("whitegrid")
        if names is not None:
            a = sns.barplot(names, self.rCloseness[:, 0], palette="BuGn_d")
        else:
            a = sns.barplot(None, self.rCloseness[:, 0], palette="BuGn_d")

        a.set_ylabel("Closeness Coeficient")
        a.set_xlabel('Alternatives')
        fig = a.get_figure()
        plt.show()

        if saveName is not None:
            fig.savefig(saveName+'.png')
