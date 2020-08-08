# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 20:18:26 2020

@author: Personal
"""

#Basic Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import re
import plotly.graph_objects as go
import random

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
    A=Data.iloc[a,]
    B=Data.iloc[b,]

    E_1,E_2=calculate_expected_score(A,B)
    #-------expected--------
    Data.loc[:,'score_ex'].iloc[a,]=Data.loc[:,'score_ex'].iloc[a,] + E_1
    Data.loc[:,'score_ex'].iloc[b,]=Data.loc[:,'score_ex'].iloc[b,] + E_2

    if won==0:
        Data.loc[:,'score_ac'].iloc[a,]=Data.loc[:,'score_ac'].iloc[a,] + 0.5
        Data.loc[:,'score_ac'].iloc[b,]=Data.loc[:,'score_ac'].iloc[b,] + 0.5
    elif won==1:
        Data.loc[:,'score_ac'].iloc[a,]=Data.loc[:,'score_ac'].iloc[a,] + 1
        Data.loc[:,'score_ac'].iloc[b,]=Data.loc[:,'score_ac'].iloc[b,] + 0
    elif won==2:
        Data.loc[:,'score_ac'].iloc[a,]=Data.loc[:,'score_ac'].iloc[a,] + 0
        Data.loc[:,'score_ac'].iloc[b,]=Data.loc[:,'score_ac'].iloc[b,] + 1
    else:
        print('Enter a suitable value for "Won"')

    Data.loc[:,'games'].iloc[a,]=Data.loc[:,'games'].iloc[a,] + 1
    Data.loc[:,'games'].iloc[b,]=Data.loc[:,'games'].iloc[b,] + 1

def bigger_better(a,b,variable):
    
    A=Data.iloc[a,]
    B=Data.iloc[b,]
    
    if A[variable] > B[variable]:
        a_against_b(a,b,1)
    elif A[variable] < B[variable]:
        a_against_b(a,b,2)
    else:
        a_against_b(a,b,0)

def less_better(a,b,variable):

    A=Data.iloc[a,]
    B=Data.iloc[b,]
    
    
    if A[variable] < B[variable]:
        a_against_b(a,b,1)
    elif A[variable] > B[variable]:
        a_against_b(a,b,2)
    else:
        a_against_b(a,b,0)





Data=pd.read_csv('H:/2020-02/How to find a new home with Scraping and game theory/Data_Final.csv') 

less=['Valor de arriendo', 'Valor de administración','Estrato','Localidad_or']
bigger=['Área construida','Habitaciones','Baños', 'Parqueadero','Área privada','Negociar Precio']

weights=[10,10,7,12,17,10,3,15,15,1]

Localidad_or=['Usaquén', 'Suba', 'Chapinero','Barrios Unidos','Teusaquillo', 
              np.nan,'La Candelaria','Fontibón','Puente Aranda','Engativá', 'Santa Fe','Kennedy','San Cristóbal','Usme','Bosa',
              'Ciudad Bolívar', 'Tunjuelito','Los Mártires','Rafael Uribe Uribe', 'Antonio Nariño']

Data['Localidad_or']=0
i=0
for l in Localidad_or:
    i=i+1
    Data['Localidad_or']=np.where(Data['Localidad']==l,i,Data['Localidad_or'])

Data['Localidad_or']=np.where(Data['Localidad'].isnull(),6,Data['Localidad_or'])    
Data['Negociar Precio']=1*Data['Negociar Precio']


Data['score_fi']=0

for champ in range(10):
    
    Data['score']=1500
    Data['score_ex']=0.0
    Data['score_ac']=0.0
    Data['games']=0.0
    
    for i in range(len(Data)*10):
        a=random.choice(range(len(Data)))
        b=random.choice(range(len(Data)))
        
        num=random.choice(range(100))
    
        for j in range(len(weights)):
            num=num-weights[j]
            if num<= 0:
                vari=less+bigger
                var=vari[j]
                break
        # a,b index of the apartments
        if var in less:
            less_better(a,b,var)
        else:
            bigger_better(a,b,var)
        pct=round(100*(i+1)/(len(Data)*10+1),2)
        print(f'-{champ}---------------------- {pct}% ---------------------------' )
        if i%len(Data)==0:
            Data['score']=update_rating(Data['score'],34,Data['score_ac'],Data['score_ex'])        
     
    Data['score_fi']=Data['score_fi']+Data['score']
    
Data['score_fi']=Data['score_fi']/40

Data.to_csv('H:/2020-02/How to find a new home with Scraping and game theory/Data_score.csv')

