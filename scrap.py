import requests
import os
import time
from bs4 import BeautifulSoup
import pandas as pd
import json

# As funções abaixo realizam uma raspagem de dados em sites que fornecem o valor do IPCA e CDI acumulado nos ultimos 12 meses


def getIpcaIBGE():
    print("Buscando valor do IPCA:", end='\t')
    url = 'https://www.ibge.gov.br/indicadores'

    req = requests.get(url)

    soup = BeautifulSoup(req.content, 'html.parser')

    # isolar o dado que queremos
    table = str(soup.find('tr', id='indicador-ipca').find('td',
                                                          class_='dozemeses').contents)
    ipca = table.split()
    ipca = ipca[5]
    ipca = float(ipca.replace(',', '.'))

    print(ipca)
    return ipca


def getIpca():
    print("Buscando valor do IPCA:", end='\t')
    url = 'https://www.melhorcambio.com/ipca'

    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(req.content, 'html.parser')

    # isolar o dado que queremos
    ipca = soup.find('input', id='indice-acum')['value']
    ipca = ipca.split()
    ipca = ipca[0]
    ipca = float(ipca.replace(',', '.'))

    print(ipca)
    return ipca


def getCdi():
    print("Buscando valor do CDI:", end='\t')
    url = 'https://www.melhorcambio.com/cdi'

    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(req.content, 'html.parser')

    # isolar o dado que queremos
    cdi = soup.find('input', id='indice-acum')['value']
    cdi = cdi.split()
    cdi = cdi[0]
    cdi = float(cdi.replace(',', '.'))

    print(cdi)
    return cdi
