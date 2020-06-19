import pandas as pd
import numpy as np
import requests 
import lxml
import time
from bs4 import BeautifulSoup
from selenium import webdriver


# Iniciar driver
options=webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument("--start-maximized")

#----------------------------------------------------------------------------
#--------------------------------Metro cuadrado ----------------------------------
#----------------------------------------------------------------------------
driver= webdriver.Chrome(executable_path=r'H:/2020-02/How to find a new home with Scraping and game theory/chromedriver.exe',options=options)
url='https://www.metrocuadrado.com/apartamentos/arriendo/bogota/'
driver.get(url)
time.sleep(10)
Links_Apt=driver.find_elements_by_xpath('//a[@class="data-details-id"]')


Lista_Urls=[]
for link in Links_Apt:
    try:
        url_new=link.get_attribute("href")
        Lista_Urls.append(url_new)
    except: 
        pass        
driver.close

data=pd.DataFrame()
i=0
for url_tem in Lista_Urls:
    
    driver= webdriver.Chrome(executable_path=r'H:/2020-02/How to find a new home with Scraping and game theory/chromedriver.exe',options=options)
    print(f'Leyendo url {i} de {len(Lista_Urls)}')
    driver.get(url_tem)
    time.sleep(8)
    #Elements
    Chara_url_temp=dict()
    try:
        #General Values
        L_GV=driver.find_element_by_xpath('.//div[@class="m_property_info_table"]').text.split('\n')
        L_GV=[x for x in L_GV if x not in ['Estoy interesado']]
        for i in range(len(L_GV)):
            if i%2==0:
                Chara_url_temp.update({L_GV[i]:[L_GV[i+1]]})
            else:
                pass         
    except:
        print('Error en General Values ')
    
    #Short desciption
    try:
        Chara_url_temp.update({'Description':[driver.find_element_by_xpath('.//p[@id="pDescription"]').text]})
    except:
        print('Error en description')
    #Property info details
    try:
        PID=driver.find_element_by_xpath('.//div[@class="m_property_info_details"]').text.split('\n')
        
        PID=[x for x in PID if x not in ['Datos principales del inmueble']]
        for i in range(len(PID)):
            if i%2==0:
                Chara_url_temp.update({PID[i]:[PID[i+1]]})
            else:
                pass   
    except:
        print('Error en Property info details ')
    
    #More info details
    try:
        MID=driver.find_element_by_xpath('.//div[@class="m_property_info_details more_info"]').text.split('\n')
        MID=[x for x in MID if x not in ['Más información de este apartamento','Ver más información']]
        for i in range(len(MID)):
            if i%2==0:
                Chara_url_temp.update({MID[i]:[MID[i+1]]})
            else:
                pass   
    except:
        print('Error en More Info details')
    #Img
    try:
        Chara_url_temp.update({'Imagen':[driver.find_element_by_xpath('.//img[@class="serviceImg horizontal-img"]').get_attribute("src")]})
    except:
        print('Error en More Imagen')


    Chara_url_temp.update({'URL':[url_tem]})

    data_tem=pd.DataFrame.from_dict(Chara_url_temp)
    data=data.append(data_tem)
    print(data_tem)
    
    print(f'Termino url {i} de {len(Lista_Urls)}')
    i=i+1
    driver.close

