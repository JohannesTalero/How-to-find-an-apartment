# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 20:47:46 2020

@author: Personal
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def del_string(self,string):
    return(str(self).replace(string,''))

def Filter(string, substr):
    return [str for str in string if 
            any(sub in str for sub in substr)]

def trate_href_barrios(barrio):
    barrio=barrio.split('title="')[1]
    barrio=barrio.split('"')[0]            
    return(barrio)

def add_barrios(UPZ,Localidad,barrio,Barrios_Total):
    data_temp=pd.DataFrame({'Unidad_Planeamiento_Zocial':[UPZ],
                                    'Localidad':[Localidad],
                                    'Barrio':[barrio]})
    Barrios_Total=Barrios_Total.append(data_temp)
    return(Barrios_Total)


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
        # Case 'y' in end of the list        
        if  len(Filter([barrio],[' y']))>0 and barrio==Barrios[-1]:
            barrio_t=barrio.split(' y')
            for b in barrio_t:
                if len(Filter([b],['/wiki/']))>0:
                    b=trate_href_barrios(b)
                Barrios_Localidad_Total=add_barrios(UPZ,Localidad,b,Barrios_Localidad_Total)
        # Case href
        elif  len(Filter([barrio],['/wiki/']))>0:
            barrio=trate_href_barrios(barrio)
        else:
            Barrios_Localidad_Total=add_barrios(UPZ,Localidad,barrio,Barrios_Localidad_Total)

Barrios_Localidad_Total=Barrios_Localidad_Total.reset_index()
del Barrios_Localidad_Total['index']

Barrios_Localidad_Total['Localidad']=Barrios_Localidad_Total['Localidad'].apply(del_string,string=' (Bogotá)') 

Barrios_Localidad_Total.to_csv("H:/2020-02/How to find a new home with Scraping and game theory/Codigo/Data_Localidades.csv")



