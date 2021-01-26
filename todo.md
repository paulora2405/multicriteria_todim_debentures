# TODO list
- Ver necessidade de conversão de Pandas Dataframe para Numpy Array [stack][stacklink]
- Corrigir variação no formato dos dados da coluna 'Índice de correção'.
- Criar método de exclusão de entradas com colunas vazias.
- Data ingestion -> web data scrapping dos índices de correção IPCA e DI (ou CDI).
- Plotar um grafico com as 10 melhores escolhas de debentures (ordenando os resultados).
- Documentar tudo

*Exemplo dos dados extraídos do csv*
```txt
   Codigo
0  AEGP13
1  AEGP23
2  AESL17
3  TIET15
4  TIET26
5  TIET27
6  TIET18
7  TIET19
8  TIET29
         Volume  Retorno 12 meses [%] Índice de correção
0  5.335000e+08                  2.42          DI + 1,4%
1  6.650000e+07                   NaN     IPCA + 7,0825%
2  2.196000e+08                   NaN        IPCA + 5,80
3  1.800000e+08                 11.54     IPCA + 6,5365%
4  3.176200e+08                  9.09     IPCA + 6,7842%
5  7.500000e+08                  2.95          DI + 1,3%
6  2.000000e+08                 12.28     IPCA + 6,0215%
7  1.380000e+09                  0.26       DI + 1,0000%
8  6.410900e+08                 14.08     IPCA + 4,7133%
```

[stacklink]: https://stackoverflow.com/questions/13187778/convert-pandas-dataframe-to-numpy-array