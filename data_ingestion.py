import numpy as np
import pandas as pd


def ingestCSV(colunas, filename='test.csv'):
    if len(colunas) < 1:
        print("Erro nos parametros de {}()".format(ingestCSV.__name__))
        raise ValueError
    try:
        raw_matrix = pd.read_csv(filename, encoding='utf-8')
        codes = raw_matrix[colunas[:1]]
        matrix = raw_matrix[colunas[1:]]
    except IOError:
        print("Erro na leitura do arquivo de entrada em ingestCSV()!")
        raise IOError

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
        print('Erro na leitura do arquivo de entrada em ingestTXT()!')
        raise IOError

    return (theta, colums, weights)

# TEST -> checar o retorno de ingestCSV()
# colunas_selecionadas = ["Codigo", "Volume",
#                         "Retorno 12 meses [%]", "Índice de correção"]
# print(ingestCSV(colunas_selecionadas)[0])
# print(ingestCSV(colunas_selecionadas)[1])


# TEST -> checar o retorno de ingestTXT()
# retorno = ingestTXT()
# print(retorno[0])
# print(retorno[1])
# print(retorno[2])
