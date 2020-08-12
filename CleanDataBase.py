#Basic Libraries
import unidecode
import Levenshtein
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import re
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = 'chrome'
#pio.renderers.default = 'browser'
#import time

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

def drop_duplicates_by_var_threshold(data,key_variable,threshold,variable_comparator='Habitaciones'):
    
    Different=pd.DataFrame(data.groupby(key_variable).count()).reset_index()
    Different=Different[Different[variable_comparator]>1]
    
    for val in Different[key_variable].unique():
        Temp=Data_Apartments[Data_Apartments[key_variable]==val]
        if simalarity(Temp)>threshold:
            index_drop=Temp.index.drop(min(Temp.index))
            data = data.drop([data.index[x] for x in index_drop])
            print(f'the indexes {index_drop} have been erased')
        else: 
            pass
    return(data)

def describe_columns_data_frame(data):
    for col in data.columns:
        print(f'################ {col} ################')
        print(data[col].describe())

def clean_variable_to_float(data,variable,strings,point_importance=False):
    for text in strings:
        data[variable]=data[variable].str.replace(text, "", case = False)
    if point_importance:
        data[variable]=pd.to_numeric(data[variable],errors='coerce')
    else:
        data[variable]=data[variable].astype('str').apply(delet_non_alphanumeric)
        data[variable]=pd.to_numeric(data[variable],errors='coerce')
    return(data[variable])
        
def del_string(self,string):
    return(str(self).replace(string,''))
#-----------------------------------------------------------------------------
path='H:/2020-02/How to find a new home with Scraping and game theory/Codigo/'
Data_Apartments=pd.read_csv(path+'Data_Apartments.csv')
del Data_Apartments['Unnamed: 0']
delete_variables_missing(Data_Apartments,0.95)
describe_columns_data_frame(Data_Apartments)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
variables_eliminate=['Estudio o biblioteca','Valor Venta','Vista','Tipo de acabado piso', 'Tipo de piso en alcobas']
for var in variables_eliminate:
    del Data_Apartments[var]

#-----------------------------------------------------------------------------
#----------------------Switch to acceptable formats---------------------------
#-----------------------------------------------------------------------------

# Clean Área construida
Data_Apartments['Área construida']=clean_variable_to_float(Data_Apartments,'Área construida',[' ','m2','de0','de'],point_importance=True)
Data_Apartments['Área construida']=np.where(Data_Apartments['Área construida']>=1000,Data_Apartments['Área construida']/100,Data_Apartments['Área construida'])

# Clean Area privada
Data_Apartments['Área privada']=clean_variable_to_float(Data_Apartments,'Área privada',[' ','m2','de0','de'],point_importance=True)
Data_Apartments['Área privada']=np.where(Data_Apartments['Área privada']>=1000,Data_Apartments['Área privada']/100,Data_Apartments['Área privada'])
Data_Apartments['Área privada']=np.where(Data_Apartments['Área privada']>=300,Data_Apartments['Área privada']/10,Data_Apartments['Área privada'])

# Clean Valor de arriendo
Data_Apartments['Negociar Precio']=(Data_Apartments['Valor de arriendo'].astype('str').apply(len_split_by_sep)>1)
Data_Apartments['Valor de arriendo']=clean_variable_to_float(Data_Apartments,'Valor de arriendo',[' Negociar Precio'])

# Clean Valor de administración
Data_Apartments['Valor de administración']=clean_variable_to_float(Data_Apartments,'Valor de administración',[''])
Data_Apartments['Valor de administración'].describe()

# Clean Número de piso
Data_Apartments['Número de piso']=clean_variable_to_float(Data_Apartments,'Número de piso',[''])
Data_Apartments['Número de piso']=np.where(Data_Apartments['Número de piso']>=100,Data_Apartments['Número de piso']/100,Data_Apartments['Número de piso'])
Data_Apartments['Número de piso']=np.where(Data_Apartments['Número de piso']>=20,Data_Apartments['Número de piso']/10,Data_Apartments['Número de piso'])

#-----------------------------------------------------------------------------
#----------------------Delete apartments and variables------------------------
#-----------------------------------------------------------------------------

#Keep case whit basic information
for var in ['Valor de arriendo','Imagen','Área construida','Estrato']:
    Data_Apartments=Data_Apartments[Data_Apartments[var].isnull() ==False]

#Posible Duplicates
for var in ['Description','Imagen']:
    Data_Apartments=drop_duplicates_by_var_threshold(Data_Apartments,var,0.85)

Data_Apartments.reset_index(drop=True,inplace=True)

#-----------------------------------------------------------------------------
#------------------------------Parkin information-----------------------------
#-----------------------------------------------------------------------------

Data_Apartments['Parqueadero']=np.where(Data_Apartments['Parqueadero'].isnull(),0,Data_Apartments['Parqueadero'])

Data_Apartments['Tipo de parqueadero']=np.where(Data_Apartments['Parqueadero']==0.0
                                                ,'NA',Data_Apartments['Tipo de parqueadero'])

Data_Apartments['Tipo de parqueadero']=np.where(Data_Apartments['Tipo de parqueadero'].isna()
                                                ,'No Reportado',Data_Apartments['Tipo de parqueadero'])

Data_Apartments['Tipo de parqueadero']=np.where(Data_Apartments['Tipo de parqueadero']=='Con servidumbre'
                                                ,'Servidumbre',Data_Apartments['Tipo de parqueadero'])

#-----------------------------------------------------------------------------
#------------------------------Del Information -------------------------------
#-----------------------------------------------------------------------------

var_del=['Tipo comedor','Conjunto cerrado', 'Tipo instalación de gas','Tipo de Cocina', 'Zona de lavanderia',
         'Área Terraza/Balcón','Características del Parqueadero','Parqueadero cubierto','Código web']
Data_Apartments=Data_Apartments[[x for x in Data_Apartments.columns if x not in var_del ]]

for c in ['Tipo de calentador','Tipo de estufa','Terraza/Balcón']:
    Data_Apartments[c]=np.where(Data_Apartments[c].isnull(),'No reportado',Data_Apartments[c])

#-----------------------------------------------------------------------------
#------------------------------ Data enrichment-------------------------------
#-----------------------------------------------------------------------------
Barrios=pd.read_csv(path+'Data_Localidades.csv',sep=',')
del Barrios['Unnamed: 0']

Data_Apartments['Barrio']=Data_Apartments['Nombre del barrio catastral']

Barrios['Barrio']=Barrios['Barrio'].str.strip()
Barrios['Barrio']=Barrios['Barrio'].str.upper()
Data_Apartments['Barrio']=Data_Apartments['Barrio'].str.upper()
Barrios['Barrio']=Barrios['Barrio'].apply(unidecode.unidecode)
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(unidecode.unidecode)

for v in ['LOS ','EL ','LAS ',' DEL ',' DE ','LA ',' I',' II',' III',' IV',' V']:
    Barrios['Barrio']=Barrios['Barrio'].apply(del_string,string=v)
    Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(del_string,string=v)

Barrios['Barrio']=Barrios['Barrio'].apply(delet_non_alphanumeric)
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(delet_non_alphanumeric)
Barrios.drop_duplicates()


Data_Apartments_En=pd.merge(Data_Apartments,Barrios,how='left',on='Barrio')
#------------------------------------------------------------------------------
for a in Data_Apartments_En[Data_Apartments_En.Localidad.isnull()]['Barrio'].unique():
    Barrios_lista=Barrios.Barrio.unique()
    min_i=1000
    barrio_prox=''
    for i in Barrios_lista:
        if (Levenshtein.distance(a, i))<min_i:
            min_i=Levenshtein.distance(a, i)
            barrio_prox=i
    print(barrio_prox)
    print(a)
    
    if True:#(min_i/len(a))<=1000:
        Localidad_temp=Barrios[Barrios['Barrio']==barrio_prox].reset_index()['Localidad'][0]
        index_temp=Data_Apartments_En[Data_Apartments_En['Barrio']==a].index[0]
        Data_Apartments_En.loc[index_temp,'Localidad']=Localidad_temp
    

Data_Apartments_En.Localidad.isnull().sum()/len(Data_Apartments_En)

Data_Apartments_En[Data_Apartments_En.Localidad.isnull()]['Barrio'].unique()

Data_Apartments_En.to_csv('H:/2020-02/How to find a new home with Scraping and game theory/Data_Final.csv')


#---------------------- Graph easy ---------------------------------------------
pio.renderers.default = 'png'
Data_Analityc_1=Data_Apartments_En[["Valor de arriendo","Área construida",'Estrato','Localidad','Habitaciones','Nombre del barrio catastral']]
Data_Analityc_1=Data_Analityc_1.groupby(["Valor de arriendo","Área construida",'Estrato','Localidad','Nombre del barrio catastral']).count().reset_index()
Data_Analityc_1=Data_Analityc_1[Data_Analityc_1["Área construida"]>=60]
Data_Analityc_1=Data_Analityc_1[Data_Analityc_1["Estrato"]>=3]
Data_Analityc_1=Data_Analityc_1[Data_Analityc_1["Estrato"]<=5]
Data_Analityc_1=Data_Analityc_1[Data_Analityc_1["Localidad"]=='Usaquén']


fig = px.scatter(Data_Analityc_1, y="Valor de arriendo", x="Área construida",color='Nombre del barrio catastral',
                 size="Habitaciones",  log_x=True,title='Área vs Valor de Arriendo')
fig.show()

#-----------------------------------------------------------------------------------


Datos=pd.read_csv('H:/2020-02/How to find a new home with Scraping and game theory/Data_Final.csv') 












