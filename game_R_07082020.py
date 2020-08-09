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
import random
from numpy.random import choice

def calculate_expected_score(apt_1,apt_2):
    R_1=apt_1.score
    R_2=apt_2.score
    E_1=1/(1+10**((R_2-R_1)/400))
    E_2=1-E_1
    return(E_1,E_2)

def update_rating(rating_0,K,current_score,E):
    R_u=rating_0+K*(current_score-E)
    return(R_u)

def a_against_b(a,b,won=0):
    """
    Parameters
    ----------
    A : TYPE
        DESCRIPTION.
    B : TYPE
        DESCRIPTION.
    won : Int, default 0
            If 0, A tied with B in the game
            If 1, A beat B in the game
            If 2, B beat B in the game

        DESCRIPTION. The default is 0.

    Returns
    -------
    None.

    """
    A=Datos.iloc[a,]
    B=Datos.iloc[b,]

    E_1,E_2=calculate_expected_score(A,B)
    #-------expected--------
    Datos.loc[:,'score_ex'].iloc[a,]=Datos.loc[:,'score_ex'].iloc[a,] + E_1
    Datos.loc[:,'score_ex'].iloc[b,]=Datos.loc[:,'score_ex'].iloc[b,] + E_2

    if won==0:
        Datos.loc[:,'score_ac'].iloc[a,]=Datos.loc[:,'score_ac'].iloc[a,] + 0.5
        Datos.loc[:,'score_ac'].iloc[b,]=Datos.loc[:,'score_ac'].iloc[b,] + 0.5
    elif won==1:
        Datos.loc[:,'score_ac'].iloc[a,]=Datos.loc[:,'score_ac'].iloc[a,] + 1
        Datos.loc[:,'score_ac'].iloc[b,]=Datos.loc[:,'score_ac'].iloc[b,] + 0
    elif won==2:
        Datos.loc[:,'score_ac'].iloc[a,]=Datos.loc[:,'score_ac'].iloc[a,] + 0
        Datos.loc[:,'score_ac'].iloc[b,]=Datos.loc[:,'score_ac'].iloc[b,] + 1
    else:
        print('Enter a suitable value for "Won"')

    Datos.loc[:,'games'].iloc[a,]=Datos.loc[:,'games'].iloc[a,] + 1
    Datos.loc[:,'games'].iloc[b,]=Datos.loc[:,'games'].iloc[b,] + 1

def bigger_better(a,b,variable):
    
    A=Datos.iloc[a,]
    B=Datos.iloc[b,]
    
    if A[variable] > B[variable]:
        a_against_b(a,b,1)
    elif A[variable] < B[variable]:
        a_against_b(a,b,2)
    else:
        a_against_b(a,b,0)

def less_better(a,b,variable):

    A=Datos.iloc[a,]
    B=Datos.iloc[b,]
    
    
    if A[variable] < B[variable]:
        a_against_b(a,b,1)
    elif A[variable] > B[variable]:
        a_against_b(a,b,2)
    else:
        a_against_b(a,b,0)




Datos=pd.read_csv('H:/2020-02/How to find a new home with Scraping and game theory/Data_Final.csv') 

less=['Valor de arriendo', 'Valor de administración','Estrato','Localidad_or']
bigger=['Área construida','Habitaciones','Baños', 'Parqueadero','Área privada','Negociar Precio']

weights=[8,13,5,10,15,10,3,13,10,13]

Localidad_or=['Usaquén', 'Suba', 'Chapinero','Barrios Unidos','Teusaquillo', 
              np.nan,'La Candelaria','Fontibón','Puente Aranda','Engativá', 'Santa Fe','Kennedy','San Cristóbal','Usme','Bosa',
              'Ciudad Bolívar', 'Tunjuelito','Los Mártires','Rafael Uribe Uribe', 'Antonio Nariño']

Datos['Localidad_or']=0
i=0
for l in Localidad_or:
    i=i+1
    Datos['Localidad_or']=np.where(Datos['Localidad']==l,i,Datos['Localidad_or'])

Datos['Localidad_or']=np.where(Datos['Localidad'].isnull(),6,Datos['Localidad_or'])    
Datos['Negociar Precio']=1*Datos['Negociar Precio']

Datos['score']=1500
Datos['score_ex']=0.0
Datos['score_ac']=0.0
Datos['games']=0.0


for i in range(len(Datos)*20):
    a=random.choice(range(len(Datos)))
    b=random.choice(range(len(Datos)))
    var=choice(less+bigger,weights)
    # a,b index of the apartments
    if var in less:
        less_better(a,b,var)
    else:
        bigger_better(a,b,var)
    pct=round(100*(i+1)/(len(Datos)*10+1),2)
    print(f'--------------------- {pct}% ---------------------------' )        

Datos['Score_f']=update_rating(Datos['score'],34,Datos['score_ac'],Datos['score_ex'])

Datos[Datos['URL']=='https://www.metrocuadrado.com/inmueble/arriendo-apartamento-bogota-urbanizacion-santa-coloma-3-habitaciones-2-banos-1-garajes/3535-1671349']
Datos['Score_f']




