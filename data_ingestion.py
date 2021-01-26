import numpy as np
import pandas as pd
from pandas.core.indexing import IndexingMixin


def ingestCSV(colunas):
    if len(colunas) < 1:
        print("Erro nos parametros de {}()".format(ingestCSV.__name__))
        raise ValueError
    raw_matrix = pd.read_csv('economatica.csv', encoding='utf-8')
    codes = raw_matrix[colunas[:1]]
    matrix = raw_matrix[colunas[1:]]

    return (codes, matrix)


def ingestTXT(filename="matriz_decisao.txt"):
    if not isinstance(filename, str):
        print("Erro nos parametros de {}()".format(ingestTXT.__name__))
        raise ValueError
    try:
        # 2 porque o comentario é contabilizado
        theta = np.loadtxt(filename, max_rows=2)
        colums = np.loadtxt(filename, max_rows=2,
                            skiprows=2, dtype=str, delimiter=",")
        weights = np.loadtxt(filename, skiprows=4)
    except IOError:
        print('Erro na leitura do arquivo de entrada!')
        raise IOError

    return (theta, colums, weights)

# colunas_selecionadas = ["Codigo", "Volume",
#                         "Retorno 12 meses [%]", "Índice de correção"]
# print(ingestCSV(colunas_selecionadas))

# filename = "matriz_decisao.txt"
# colums = np.loadtxt(filename, max_rows=2, skiprows=2, dtype=str, delimiter=",")
# print(colums)


# print(type(ingestTXT()))  # => <class 'tuple'>
