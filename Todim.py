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

        # normalizar os pesos
        if self.weights.sum() > 1.001 or self.weights.sum() < 0.9999:
            self.weights = self.weights/self.weights.sum()

        # inicializar as variaveis
        tam = self.matrixD.shape
        [self.nAlt, self.nCri] = tam
        self.normMatrixD = np.zeros(tam, dtype=float)
        self.delta = np.zeros([self.nAlt, self.nCri])
        self.rCloseness = np.zeros([self.nAlt, 1], dtype=float)
        # peso de referencia
        self.wref = self.weights.max()
