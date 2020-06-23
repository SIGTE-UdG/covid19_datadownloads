import git
import os
import pandas as pd
import datetime
import shutil
import sys
from subprocess import Popen, PIPE
from datetime import datetime, date, time, timedelta
import numpy as np
import requests

import csv


# directorio en el que guardar los datos
path = '/tmp/'

# identificación y código oficial de las CCAA
codi_ccaa = ['AN','AR','AS','IB','CN','CB','CL','CM','CT','VC','EX','GA','MD','MC','NC','PV','RI','CE','MC']
ccaa_id = {'CCAA': codi_ccaa, 'CODI': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]}

# lista con la tabla de datos
llista_dades = []

# descarga de los datos en formato CSV
url = 'https://cnecovid.isciii.es/covid19/resources/agregados.csv'
response = requests.get(url)
if response.status_code != 200:
    print('Failed to get data:', response.status_code)
else:
    wrapper = csv.reader(response.text.strip().split('\n'))
    for record in wrapper:
        res1 = any(record[0] in sublist for sublist in codi_ccaa)
        if str(res1) == 'True':
            llista_dades.append(record)


# creamos un data frame de pandas a partir del array con los datos
dades = pd.DataFrame(llista_dades)
dades.columns = ['CCAA', 'FECHA', 'CASOS', 'PCR', 'TestAc','Hospitalizados','UCI', 'Fallecidos']


# renombramos las columnas del dataframe
dades.rename(columns={'UCI':'icu'}, inplace=True)
dades.rename(columns={'Hospitalizados':'hospitalized'}, inplace=True)
dades.rename(columns={'PCR.':'pcr'}, inplace=True)
dades.rename(columns={'TestAc.':'test'}, inplace=True)
dades.rename(columns={'FECHA':'date'}, inplace=True)
dades.rename(columns={'Recuperados':'recovered'}, inplace=True)
dades.rename(columns={'Fallecidos':'casualty'}, inplace=True)
dades.rename(columns={'CASOS':'cases'}, inplace=True)


# el índice del dataframe será la columna con el nombre de las CCAA
dades.set_index('CCAA', inplace=True)

# añadimos al datafreme una columna con el código oficial de cada CCAA
# utilizamos un merge para hacer esta unión.
ccaa_id_frame = pd.DataFrame.from_dict(ccaa_id)
dades_final = dades.merge(ccaa_id_frame, left_on='CCAA', right_on='CCAA')

# renombramos campos del dataframe y cambiamos el índice
dades_final.rename(columns={'CODI':'ccaa_id'}, inplace=True)

dades_final.set_index('ccaa_id', inplace=True)

del dades_final['CCAA']

# mostramos por pantalla el resultado de la tabla
print(dades_final)

# guardamos el dataframe en un fiechero .csv
dades_final.to_csv(path +'dades_covid19.csv')


print("Arxiu generat correctament")
