import requests
import os
import time
from bs4 import BeautifulSoup
import pandas as pd
import json

# ipca = None
# di = None


def getIpca():

    url = 'https://www.ibge.gov.br/indicadores'

    req = requests.get(url)

    soup = BeautifulSoup(req.content, 'html.parser')

    table = str(soup.find('tr', id='indicador-ipca').find('td',
                                                          class_='dozemeses').contents)
    ipca = table.split()
    ipca = ipca[5]
    ipca = float(ipca.replace(',', '.'))

    return ipca


def getCdi():

    url = 'https://www.melhorcambio.com/cdi'

    req = requests.get(url)

    soup = BeautifulSoup(req.content, 'html.parser')

    table = soup.find('div', class_='holder-valor')
    print(soup)

    # cdi = table.split()
    # cdi = cdi[5]
    # cdi = float(cdi.replace(',', '.'))

    # return cdi


getCdi()
# def old():

#    for page in pages:
#         url = 'https://loja.asus.com.br/ofertas?p=' + page

#         req = requests.get(url)

#         soup = BeautifulSoup(req.content, 'html.parser')

#         lista_produtos = soup.find_all('div', class_='regular')

#         for lista_titulos in lista_produtos:
#             lista = lista_titulos.find_all('div', class_='product-info')

#             for lista_dados in lista:
#                 titulo = lista_dados.find(
#                     'a', class_='product-name').get('title')
#                 valor = lista_dados.find(
#                     'p', class_='special-price').find('span', class_='price')

#                 # há dois tipos de estruturas para representar o valor
#                 if(valor.find('span', class_='price') != None):
#                     valor = valor.find('span', class_='price').next_element
#                 else:
#                     valor = valor.next_element.split(' ')[-1]
#                     valor = valor.split('\t')[0]
#                 prices.append(valor)
#                 titles.append(titulo)

#     df = pd.DataFrame({'price': prices, 'title': titles})

#     df.to_string('products.txt')
