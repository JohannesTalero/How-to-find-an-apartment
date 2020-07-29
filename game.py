# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 20:18:26 2020

@author: Personal
"""

#Basic Libraries
import unidecode
import Levenshtein
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import re
import plotly.graph_objects as go

# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'H:/2020-02/How to find a new home with Scraping and game theory/Codigo/')

import class_def as apt


def column_to_apartment(Datos,i):
    
    #Define physical properties
    built_area=Datos['Área construida'].iloc[i]
    private_area=Datos['Área privada'].iloc[i]
    rooms=Datos['Habitaciones'].iloc[i]
    bathrooms=Datos['Baños'].iloc[i]
    floors=Datos['Número de piso'].iloc[i]
    time=Datos['Tiempo de construido'].iloc[i]
    
    physical=apt.physical_properties(built_area, private_area, rooms, bathrooms, floors, time)
    
    #Define contextual properties
    common_neighborhood=Datos['Nombre común del barrio'].iloc[i]
    cadastral_neighborhood=Datos['Nombre del barrio catastral'].iloc[i]
    localidad=Datos['Localidad'].iloc[i]
    stratum=Datos['Estrato'].iloc[i]
    
    contextual=apt.contextual_properties(common_neighborhood, cadastral_neighborhood, localidad, stratum)
    
    #Define parking properties
    parking=Datos['Parqueadero'].iloc[i]
    kind=Datos['Tipo de parqueadero'].iloc[i]
    deposit=Datos['Depósitos'].iloc[i]
    parking=apt.parking_properties(parking, kind, deposit)
    
    #Define parking properties
    Heater=Datos['Tipo de calentador'].iloc[i]
    terrace=Datos['Terraza/Balcón'].iloc[i]
    stove=Datos['Tipo de estufa'].iloc[i]
    
    additional=apt.additional_properties(Heater, terrace, stove)
    
    #Define apartment
    Lease_value=Datos['Valor de arriendo'].iloc[i]
    Administration_value=Datos[ 'Valor de administración'].iloc[i]
    Description=Datos['Description'].iloc[i]
    Image=Datos['Imagen'].iloc[i]
    URL=Datos['URL'].iloc[i]
    Negotiate_Price=Datos['Negociar Precio'].iloc[i]
    
    apartment=apt.apartment(Lease_value, Administration_value, Description, Image, URL, Negotiate_Price, physical, contextual, parking, additional)
    return({URL:apartment})


Datos=pd.read_csv('H:/2020-02/How to find a new home with Scraping and game theory/Data_Final.csv') 
dic_apartment=dict()
for i in range(len(Datos)):
    dic_apartment.update(column_to_apartment(Datos,i))

key_1=list(dic_apartment.keys())[0]
key_2=list(dic_apartment.keys())[1]

dic_apartment[key_1].score
dic_apartment[key_2]


