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
Data_Apartments['Área construida'].describe()

# Clean Area privada
Data_Apartments['Área privada']=clean_variable_to_float(Data_Apartments,'Área privada',[' ','m2','de0','de'],point_importance=True)
Data_Apartments['Área privada']=np.where(Data_Apartments['Área privada']>=1000,Data_Apartments['Área privada']/100,Data_Apartments['Área privada'])
Data_Apartments['Área privada']=np.where(Data_Apartments['Área privada']>=300,Data_Apartments['Área privada']/10,Data_Apartments['Área privada'])
Data_Apartments['Área privada'].describe()

# Clean Valor de arriendo
Data_Apartments['Negociar Precio']=(Data_Apartments['Valor de arriendo'].astype('str').apply(len_split_by_sep)>1)
Data_Apartments['Valor de arriendo']=clean_variable_to_float(Data_Apartments,'Valor de arriendo',[' Negociar Precio'])
Data_Apartments['Valor de arriendo'].describe()

# Clean Valor de administración
Data_Apartments['Valor de administración']=clean_variable_to_float(Data_Apartments,'Valor de administración',[''])
Data_Apartments['Valor de administración'].describe()

# Clean Número de piso
Data_Apartments['Número de piso']=clean_variable_to_float(Data_Apartments,'Número de piso',[''])
Data_Apartments['Número de piso']=np.where(Data_Apartments['Número de piso']>=100,Data_Apartments['Número de piso']/100,Data_Apartments['Número de piso'])
Data_Apartments['Número de piso']=np.where(Data_Apartments['Número de piso']>=20,Data_Apartments['Número de piso']/10,Data_Apartments['Número de piso'])
Data_Apartments['Número de piso'].describe()

#-----------------------------------------------------------------------------
#----------------------Delete apartments and variables------------------------
#-----------------------------------------------------------------------------

#Keep case whit basic information
Data_Apartments=Data_Apartments[Data_Apartments['Valor de arriendo'].isnull() ==False]
Data_Apartments=Data_Apartments[Data_Apartments['Imagen'].isnull() ==False]
Data_Apartments=Data_Apartments[Data_Apartments['Área construida'].isnull() ==False]
Data_Apartments=Data_Apartments[Data_Apartments['Estrato'].isnull() ==False]

Data_Apartments=Data_Apartments.reset_index()
del Data_Apartments['index']
del Data_Apartments['Código web']

#Posible Duplicates
Data_Apartments=drop_duplicates_by_var_threshold(Data_Apartments,'Description',0.85)
Data_Apartments=drop_duplicates_by_var_threshold(Data_Apartments,'Imagen',0.85)

Data_Apartments=Data_Apartments.reset_index()
del Data_Apartments['index']

#-----------------------------------------------------------------------------
#------------------------------Parkin information-----------------------------
#-----------------------------------------------------------------------------

del Data_Apartments['Características del Parqueadero']
del Data_Apartments['Parqueadero cubierto']

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

del Data_Apartments['Tipo comedor']
del Data_Apartments['Conjunto cerrado']
del Data_Apartments['Tipo instalación de gas']
del Data_Apartments['Tipo de Cocina']
del Data_Apartments['Zona de lavanderia'] 
del Data_Apartments['Área Terraza/Balcón']

Data_Apartments['Tipo de calentador']=np.where(Data_Apartments['Tipo de calentador'].isnull(),'No reportado',Data_Apartments['Tipo de calentador'])
Data_Apartments['Tipo de estufa']=np.where(Data_Apartments['Tipo de estufa'].isnull(),'No reportado',Data_Apartments['Tipo de estufa'])
Data_Apartments['Terraza/Balcón']=np.where(Data_Apartments['Terraza/Balcón'].isnull(),'No reportado',Data_Apartments['Terraza/Balcón'])

#-----------------------------------------------------------------------------
#------------------------------ Data enrichment-------------------------------
#-----------------------------------------------------------------------------
Barrios=pd.read_csv(path+'Data_Localidades.csv',sep=',')
del Barrios['Unnamed: 0']
Barrios['Barrio']=Barrios['Barrio'].str.strip()
Barrios['Barrio']=Barrios['Barrio'].str.upper()
Barrios['Barrio']=Barrios['Barrio'].apply(unidecode.unidecode)
Barrios['Barrio']=Barrios['Barrio'].apply(del_string,string='LOS ')
Barrios['Barrio']=Barrios['Barrio'].apply(del_string,string='EL ')
Barrios['Barrio']=Barrios['Barrio'].apply(del_string,string='LAS ')
Barrios['Barrio']=Barrios['Barrio'].apply(del_string,string=' DEL ')
Barrios['Barrio']=Barrios['Barrio'].apply(del_string,string=' DE ')
Barrios['Barrio']=Barrios['Barrio'].apply(del_string,string='LA ')
Barrios['Barrio']=Barrios['Barrio'].apply(del_string,string=' I')
Barrios['Barrio']=Barrios['Barrio'].apply(del_string,string=' II')
Barrios['Barrio']=Barrios['Barrio'].apply(del_string,string=' III')
Barrios['Barrio']=Barrios['Barrio'].apply(del_string,string=' IV')
Barrios['Barrio']=Barrios['Barrio'].apply(del_string,string=' V')
Barrios['Barrio']=Barrios['Barrio'].apply(delet_non_alphanumeric)
Barrios.drop_duplicates()

Data_Apartments['Barrio']=Data_Apartments['Nombre del barrio catastral']
Data_Apartments['Barrio']=Data_Apartments['Barrio'].str.upper()
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(unidecode.unidecode)
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(del_string,string='LOS ')
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(del_string,string='EL ')
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(del_string,string='LAS ')
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(del_string,string=' DEL ')
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(del_string,string=' DE ')
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(del_string,string='LA ')
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(del_string,string=' I')
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(del_string,string=' II')
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(del_string,string=' III')
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(del_string,string=' IV')
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(del_string,string=' V')
Data_Apartments['Barrio']=Data_Apartments['Barrio'].apply(delet_non_alphanumeric)

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












