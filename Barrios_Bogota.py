# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 20:47:46 2020

@author: Personal
"""

import requests
from bs4 import BeautifulSoup

def del_string(self,string):
    return(str(self).replace(string,''))

url='https://es.wikipedia.org/wiki/Anexo:Barrios_de_Bogot%C3%A1'
website_url = requests.get(url).text

soup = BeautifulSoup(website_url,'lxml')
My_table = soup.find('table',{'class':'wikitable sortable'})

Barrios_Localidad_Total=pd.DataFrame()

for i in range(len(My_table.findAll('tr'))-1):
    UPZ=str(My_table.findAll('tr')[i+1].findAll('td')[1]).replace('<td>','')
    UPZ=UPZ.replace('\n</td>','')
    
    Localidad=str(My_table.findAll('tr')[i+1].findAll('td')[2]).split('"')[3].replace('<td>','')
    Localidad=Localidad.replace('\n</td>','')
    
    Barrios=str(My_table.findAll('tr')[i+1].findAll('td')[3]).replace('<td>','')
    Barrios=Barrios.replace('\n</td>','')
    Barrios=Barrios.split(',')
    
    for barrio in Barrios:
        data_temp=pd.DataFrame({'Unidad_Planeamiento_Zocial':[UPZ],
                                'Localidad':[Localidad],
                                'Barrio':[barrio]})
        Barrios_Localidad_Total=Barrios_Localidad_Total.append(data_temp)

Barrios_Localidad_Total=Barrios_Localidad_Total.reset_index()
del Barrios_Localidad_Total['index']

Barrios_Localidad_Total['Localidad']=Barrios_Localidad_Total['Localidad'].apply(del_string,string=' (Bogotá)') 
Barrios_Localidad_Total['Localidad']=Barrios_Localidad_Total['Localidad'].apply(del_string,string=' (Bogotá)') 
    
Barrios_Localidad_Total['Localidad']s
wiki






