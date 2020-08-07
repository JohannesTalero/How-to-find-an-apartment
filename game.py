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

def calculate_expected_score(apt_1,apt_2):
    R_1=apt_1.score
    R_2=apt_2.score
    E_1=1/(1+10**((R_2-R_1)/400))
    E_2=1-E_1
    return(E_1,E_2)

def update_rating(rating_0,K,current_score,E):
    R_u=rating_0+K*(current_score-E)
    return(R_u)

def a_against_b(A,B,won=0):
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
    E_1,E_2=calculate_expected_score(A,B)
    #-------expected--------
    A.score_ex=A.score_ex + E_1
    B.score_ex=B.score_ex + E_2
    if won==0:
        A.score_ac=A.score_ac + 0.5
        B.score_ac=B.score_ac + 0.5        
    elif won==1:
        A.score_ac=A.score_ac + 1
        B.score_ac=B.score_ac + 0        
    elif won==2:
        A.score_ac=A.score_ac + 0
        B.score_ac=B.score_ac + 1        
    else:
        print('Enter a suitable value for "Won"')
    A.games=A.games+1
    B['games']=B['games']+1

def bigger_better(A,B,variable):
    
    if A[variable] > B[variable]:
        a_against_b(A,B,1)
    elif A[variable] < B[variable]:
        a_against_b(A,B,2)
    else:
        a_against_b(A,B,0)

def less_better(A,B,variable):
    
    if A[variable] < B[variable]:
        a_against_b(A,B,1)
    elif A[variable] > B[variable]:
        a_against_b(A,B,2)
    else:
        a_against_b(A,B,0)




Datos=pd.read_csv('H:/2020-02/How to find a new home with Scraping and game theory/Data_Final.csv') 

less=['Valor de arriendo', 'Valor de administración','Estrato']
bigger=['Área construida','Habitaciones','Baños', 'Parqueadero','Área privada','Negociar Precio']


Datos['Negociar Precio']=1*Datos['Negociar Precio']
Datos['score']=1500
Datos['score_ex']=0
Datos['score_ac']=0
Datos['games']=0
Datos.iloc[2,-1]=2
B=Datos.iloc[3,]

for i in range(10):

    var=random.choice(less+bigger)
    print(var)
    if var in less:
        less_better(Datos.iloc[2,],Datos.iloc[3,],var)
    else:
        bigger_better(Datos.iloc[2,],Datos.iloc[3,],var)
        
    





 










