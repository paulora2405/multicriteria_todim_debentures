from numpy.matrixlib.defmatrix import matrix
import pandas as pd
from tabulate import tabulate as tb

raw_matrix = pd.read_csv('economatica.csv', encoding='utf-8')

matrix = raw_matrix[["Codigo", "Volume",
                     "Retorno 12 meses [%]", "Índice de correção"]]

print(matrix)

# arq = open()
