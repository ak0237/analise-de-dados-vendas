# -*- coding: utf-8 -*-
"""vendas.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14NAZG3rNzigiiZKb7XvRfONGcpJWRUKz

#Preparando o ambiente

##Importando as bibliotecas
"""

import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None)  # Mostra todas as linhas

"""##Importando o csv"""

urli = 'https://raw.githubusercontent.com/KeithGalli/Pandas-Data-Science-Tasks/refs/heads/master/SalesAnalysis/Sales_Data/Sales_'
urlf = '_2019.csv'

meses = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

todos_meses = pd.DataFrame()

for mes in meses:
    #print(urli + mes + urlf)
    df = pd.read_csv(urli + mes + urlf)
    todos_meses = pd.concat([todos_meses, df])

todos_meses.head()

"""#Limpando os dados

##Removendo NaNs
"""

#nan_df = todos_meses[todos_meses.isna().any(axis=1)]
#nan_df.head()

todos_meses = todos_meses.dropna(how='all')
#todos_meses.head()

"""##Tratando a coluna 'Order Date'"""

tdf = todos_meses[todos_meses['Order Date'].str[0:2] == 'Or']
tdf.head()
todos_meses = todos_meses[todos_meses['Order Date'].str[0:2] != 'Or']

"""##Convertendo as colunas necessárias para tipos numéricos"""

todos_meses['Quantity Ordered'] = pd.to_numeric(todos_meses['Quantity Ordered'])
todos_meses['Price Each'] = pd.to_numeric(todos_meses['Price Each'])
todos_meses.info()

"""##Criando uma coluna chamada 'Mes' e populando-a com os dadis extraído da coluna 'Order Date'"""

todos_meses['Mes'] = todos_meses['Order Date'].str[0:2]
todos_meses['Mes'] = todos_meses['Mes'].astype('int8')
todos_meses.head()

todos_meses['Mes'].unique()

"""#Avaliando as vendas

##Criando uma colua 'Sales' que indica o valor de vendas de cada compra
"""

todos_meses['Sales'] = todos_meses['Quantity Ordered'] * todos_meses['Price Each']
todos_meses.head()

"""##Avaliando as vendas de cada mês"""

todos_meses.groupby('Mes')['Sales'].sum()

"""###Plotando gráfico"""

plt.bar(range(1, 13), todos_meses.groupby('Mes')['Sales'].sum())
plt.xticks(range(1, 13))
plt.xlabel('Mes')
plt.ylabel('Vendas')
plt.show()

"""##Criando uma coluna que indica a cidade do cliente que realizou cada compra"""

def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(" ")[1]

todos_meses['Cidade'] = todos_meses['Purchase Address'].apply(lambda x : get_city(x) + ' ' + get_state(x))

#todos_meses = todos_meses.drop(columns=['Estado Zip', 'Rua'])
#todos_meses.head()

#todos_meses['Purchase Address'].str.split(',', expand=True)
#todos_meses[['Rua', 'Cidade', 'Estado']] = todos_meses['Purchase Address'].str.split(',', expand=True)
#todos_meses.drop(columns='Pais', inplace=True)
todos_meses.head()

"""##Criando um DF agrupado por cidade"""

results = todos_meses.groupby('Cidade').sum()
results.head()

"""###Plotando o gráfico de vendas por cidade"""

cidades = [cidade for cidade, df in todos_meses.groupby('Cidade')]
plt.bar(cidades, results['Sales'])
plt.xticks(rotation='vertical', size=8)
plt.xlabel('Cidade')
plt.ylabel('Vendas')
plt.show()

"""##Convertendo a coluna 'Order Date' para datetime"""

todos_meses['Order Date'] = pd.to_datetime(todos_meses['Order Date'])
#order_dates = pd.to_datetime(todos_meses['Order Date'])
#todos_meses['Hora'] = order_dates.dt.hour
#todos_meses['Minuto'] = order_dates.dt.minute
todos_meses.head()

"""###Criando e populando as colunas 'Hora' e 'Minuto'"""

todos_meses['Hora'] = todos_meses['Order Date'].dt.hour
todos_meses['Minuto'] = todos_meses['Order Date'].dt.minute
todos_meses.head()

"""####Plotando um gráfico que relaciona a quantidade de vendas feitas por hora"""

horas = [hora for hora, df in todos_meses.groupby('Hora')]
plt.plot(horas, todos_meses.groupby(['Hora']).count())
plt.xticks(horas)
plt.xlabel('Hora')
plt.ylabel('Quantidade')
plt.grid()
plt.show()

todos_meses.head()

