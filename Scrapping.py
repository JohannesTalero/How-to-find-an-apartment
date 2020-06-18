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

#brikss.com
driver= webdriver.Chrome(executable_path=r'H:/2020-02/How to find a new home with Scraping and game theory/Codigo/chromedriver.exe',options=options)
url='https://www.brikss.com/residencial?o=arriendo'
driver.get(url)
time.sleep(10)
Links_Apt=driver.find_elements_by_xpath('//div[@class="inmueblePreview cirugia"]')

Lista_Urls=[]
for link in Links_Apt:
    try:
        codigo_mobile=link.find_element_by_xpath('.//div[@class="codigo-mobile"]').text.split('\n')[1]
        url_new='https://www.brikss.com/inmueble/'+codigo_mobile+'?o=comprar'
        Lista_Urls.append(url_new)
    except: 
        pass        

data=pd.DataFrame()

for url_tem in Lista_Urls:
    driver.get(url_tem)
    time.sleep(10)
    chars1=driver.find_elements_by_xpath('.//div[@class="charItem"]')
    Chara_url_temp=dict()
    for char in chars1:
        Chara_url_temp.update({char.text.split('\n')[1]:[char.text.split('\n')[0]]})
    Chara_url_temp.update({'URL':[url_tem]})
    data_tem=pd.DataFrame.from_dict(Chara_url_temp)
    data.append(date_tem)
    print(data_tem)






driver.close

