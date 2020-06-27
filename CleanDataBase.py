# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 21:51:45 2020

@author: Personal
"""

#Basic Libraries
import pandas as pd
import numpy as np
import re
import time

def delete_variables_missing(data,threshold):
    describe_missing=pd.DataFrame(data.isnull().sum()/len(data)).reset_index()
    describe_missing_var=describe_missing[describe_missing[0]>=threshold]['index']
    for var in describe_missing_var:
        del data[var]

def Filter(string, substr): 
    return [str for str in string if
             any(sub in str for sub in substr)] 

def len_split_by_sep(string,sep=' '):
    return(len(string.split(sep)))

def delet_non_alphanumeric(string):
    return (re.sub("[^0-9a-zA-Z]+", "", string))

def simalarity(Temp):    
    similar_variables=0
    for col in Temp.columns:
        if len(Temp.groupby(col).count()) <= 1:
            similar_variables=similar_variables+1
    similarity_coe=(similar_variables-1)/(len(Temp.columns)-2)
    return(similarity_coe) 

path='H:/2020-02/How to find a new home with Scraping and game theory/Codigo/Data_Apartments.csv'
Data_Apartments=pd.read_csv(path)

#Just keep case whit basic information
Data_Apartments=Data_Apartments[Data_Apartments['Valor de arriendo'].isnull() ==False]
Data_Apartments=Data_Apartments[Data_Apartments['Imagen'].isnull() ==False]
Data_Apartments=Data_Apartments[Data_Apartments['Área construida'].isnull() ==False]
Data_Apartments=Data_Apartments[Data_Apartments['Baños'].isnull() ==False]

delete_variables_missing(Data_Apartments,0.95)

pd.DataFrame(Data_Apartments.isnull().sum()/len(Data_Apartments)).reset_index()
del Data_Apartments['Unnamed: 0']

# Clean Área construida
Data_Apartments['Área construida']=Data_Apartments['Área construida'].str.replace(" m2", "", case = False)
Data_Apartments['Área construida']=Data_Apartments['Área construida'].str.replace(" de", "", case = False)
Data_Apartments['Área construida']=Data_Apartments['Área construida'].str.replace("de 0", "", case = False)
Data_Apartments['Área construida']=Data_Apartments['Área construida'].str.replace(" ", "", case = False)
Data_Apartments['Área construida']=pd.to_numeric(Data_Apartments['Área construida'],errors='coerce')
Data_Apartments['Área construida']=np.where(Data_Apartments['Área construida']>=1000,Data_Apartments['Área construida']/100,Data_Apartments['Área construida'])
Data_Apartments['Área construida'].describe()

# Clean Área  Valor de arriendo
Data_Apartments['Negociar Precio']=(Data_Apartments['Valor de arriendo'].apply(len_split_by_sep)>1)
Data_Apartments['Valor de arriendo']=Data_Apartments['Valor de arriendo'].str.replace(" Negociar Precio", "", case = False)
Data_Apartments['Valor de arriendo']=Data_Apartments['Valor de arriendo'].apply(delet_non_alphanumeric)
Data_Apartments['Valor de arriendo']=pd.to_numeric(Data_Apartments['Valor de arriendo'],errors='coerce')
Data_Apartments['Valor de arriendo'].describe()







#Posible Duplicates 
Different=pd.DataFrame(Data_Apartments.groupby('Description').count()).reset_index()
Different=Different[Different['Habitaciones']>1]

for val in Different['Description'].unique():
    Temp=Data_Apartments[Data_Apartments['Description']==val]
    print(simalarity(Temp))
    print(len(Temp))


Temp
similar_variables=0

   
    






len(Data_Apartments.Description.unique())/len(Data_Apartments)