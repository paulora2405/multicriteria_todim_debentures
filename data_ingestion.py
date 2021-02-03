import numpy as np
import pandas as pd
import scrap

# Carrega do arquivo .txt o valor de theta, os pesos dos criterios, o nome de cada criterio, e os filtros (se existirem)


def ingestTXT(filename="matriz_decisao.txt"):
    print("Importando o .txt")
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

# busca os dados das colunas que foram requeridas no arquivo .txt no arquivo .csv onde se encontram os dados


def ingestCSV(colunas, filename='economatica.csv'):
    print("Importando o .csv")
    if len(colunas) < 1:
        print("Erro nos parametros de {}()".format(ingestCSV.__name__))
        raise ValueError
    try:
        raw_matrix = pd.read_csv(filename, encoding='utf-8')

        # faz a exclusão das linhas que contem algum valor numerico nulo.
        raw_matrix.dropna(
            subset=['Volume', 'Retorno 12 meses [%]'], inplace=True)
        # reseta o indice da matriz numpy
        raw_matrix.reset_index(inplace=True)

        # "codes" são as abreviações de cada debenture, elas só serão usadas para se mostrar os resultados ao final
        codes = raw_matrix[colunas[:1]]
        matrix = raw_matrix[colunas[1:]]

        # a coluna "Índice de correção" possui por exemplo o formato "IPCA + 3%" o valor do IPCA deve ser buscado nesse caso
        if ("Índice de correção" in colunas):
            applyIndex(matrix)

    except IOError:
        print("Erro na leitura do arquivo de entrada em ingestCSV()!")
        raise IOError

    return (codes, matrix)


# converte "IPCA + 3%" para "7.0" caso o valor do IPCA seja 4, por exemplo
def applyIndex(matrix):
    indice_str = "Índice de correção"
    print("Aplicando DI e IPCA aos índices de correção")
    indices = matrix["Índice de correção"]

    # busca o valor do IPCA e do CDI
    di = scrap.getCdi()
    ipca = scrap.getIpca()

    for i in range(len(indices)):
        if indices[i].split('+')[0].strip() == 'DI':  # DI Spread
            s = indices[i].split('+')
            s = s[-1].strip()[:-1]
            s = s.replace(',', '.')
            s = float(s)
            s = di + s
        elif indices[i].split('+')[0].strip() == 'IPCA':  # IPCA Spread
            s = indices[i].split('+')
            s = s[-1].strip()[:-1]
            s = s.replace(',', '.')
            s = float(s)
            s = ipca + s
        else:  # DI Percentual
            s = indices[i].lower().split('d')
            s = s[0].strip()[:-1]
            s = s.replace(',', '.')
            s = float(s)
            s = di * s/100
        matrix.at[i, indice_str] = s
