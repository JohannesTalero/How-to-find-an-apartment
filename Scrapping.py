#Basic Libraries
import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
#----------------------------------------------------------------------------
#-------------------------------- Function ----------------------------------
#----------------------------------------------------------------------------
def get_dpt_links(driver):
    """Returns the list of apartments found on the page
    Parameters
    ----------
    driver : webdriver
        It is the driver in which the apartments are searched.
    Returns
    -------
    array of apartment if an error occurs it returns an empty array.

    """
    try:
        object_link=driver.find_elements_by_xpath('//a[@class="data-details-id"]')
        Links_Apt=[]
        for obj in object_link:            
            url_new=obj.get_attribute("href")
            Links_Apt=Links_Apt+[url_new]
    except:
        print('An unexpected error has appeared in the apartment list search')
        Links_Apt=[]
    return(Links_Apt)

def smart_delay(driver,delay,xpathx_str):
    """ Pauses intelligently until xpathx_str appears, waiting for a maximum of delay,
        if xpathx_str does not occur, an error returns.    
    Parameters
    ----------
    driver : webdriver
        It is the driver in which the departments are searched..
    delay : int
        The maximum waiting time in seconds.
    xpathx_str : string
        the waiting xpath object.

    Returns
    -------
    None.

    """
    # Introducir una demora
    delay = 10
    try:
        departments_page = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH,xpathx_str )))
        print(' finished loading')
    except TimeoutException as e:
        return(e)

def general_values(driver,Chara_url_temp):
    """
    Return the general values of the apartments
    ----------
    driver : webdriver
        It is the driver in which the departments are searched..
    Chara_url_temp : Dictionary
        Dictionary that saves the apartment data.

    Returns
    -------
    None.

    """
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

def short_description(driver,Chara_url_temp):
    """
    Return the short description of the apartments
    ----------
    driver : webdriver
        It is the driver in which the departments are searched..
    Chara_url_temp : Dictionary
        Dictionary that saves the apartment data.

    Returns
    -------
    None.

    """
    #Short desciption
    try:
        Chara_url_temp.update({'Description':[driver.find_element_by_xpath('.//p[@id="pDescription"]').text]})
    except:
        print('Error en description')
        
def property_info_details(driver,Chara_url_temp):
    """
    Return the property info details of the apartments
    ----------
    driver : webdriver
        It is the driver in which the departments are searched..
    Chara_url_temp : Dictionary
        Dictionary that saves the apartment data.

    Returns
    -------
    None.

    """
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
    
def more_info_details(driver,Chara_url_temp):
    """
    Return the more info detail of the apartments
    ----------
    driver : webdriver
        It is the driver in which the departments are searched..
    Chara_url_temp : Dictionary
        Dictionary that saves the apartment data.

    Returns
    -------
    None.

    """
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
        
def imagen_apt(driver,Chara_url_temp):
    """
    Return the url imagen of the apartments
    ----------
    driver : webdriver
        It is the driver in which the departments are searched..
    Chara_url_temp : Dictionary
        Dictionary that saves the apartment data.

    Returns
    -------
    None.

    """
    #Img
    try:
        Chara_url_temp.update({'Imagen':[driver.find_element_by_xpath('.//img[@class="serviceImg horizontal-img"]').get_attribute("src")]})
    except:
        print('Error en More Imagen')
    
   
def get_information(driver,Chara_url_temp):
    """
    Return the informatio of the apartments
    ----------
    driver : webdriver
        It is the driver in which the departments are searched..
    Chara_url_temp : Dictionary
        Dictionary that saves the apartment data.
    Returns
    -------
    None.
    """
    general_values(drive, Chara_url_temp)
    short_description(drive, Chara_url_temp)
    property_info_details(drive, Chara_url_temp)
    more_info_details(drive, Chara_url_temp) 
    imagen_apt(drive, Chara_url_temp)

#----------------------------------------------------------------------------
#--------------------------------Metro cuadrado -----------------------------
#----------------------------------------------------------------------------

#Driver initilizer
options=webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument("--start-maximized")
#options.add_argument('--proxy-server=%s' % proxy[0])

driver= webdriver.Chrome(executable_path=r'H:/2020-02/How to find a new home with Scraping and game theory/chromedriver.exe',options=options)
url='https://www.metrocuadrado.com/apartamentos/arriendo/bogota/'
driver.get(url)
smart_delay(driver,10,'//div[@class="button"]')

#Select options with 3 rooms
rooms_3=driver.find_elements_by_xpath('//div[@class="button"]')[2]
ActionChains(driver).click(rooms_3).perform()
#Select options with 2 rooms
#time.sleep(10)
#rooms_2=driver.find_elements_by_xpath('//div[@class="button"]')[1]
#ActionChains(driver).click(rooms_2).perform()

Price_l=driver.find_element_by_xpath('//input[@id="list-price_from"]')
Price_u=driver.find_element_by_xpath('//input[@id="list-price_to"]')
Price_l.send_keys("1000000")
Price_u.send_keys("2000000")

button_price=driver.find_element_by_xpath('//a[@class="m_btn inline inverted price_range"]')
ActionChains(driver).click(button_price).perform()

#Apartment url search
more=True
i=0
Full_links=[]
while more:
    i=i+1
    try:
        smart_delay(driver,30,'//a[@class="next list"]')
        smart_delay(driver,10,'//a[@class="data-details-id"]')
        Links_Temp=get_dpt_links(driver)
        Full_links=Full_links+Links_Temp
        #Click for next page 
        try:
            next_page=driver.find_element_by_xpath('//a[@class="next list"]')
            ActionChains(driver).click(next_page).perform()
            if len(Full_links)>20000:
                more=False                
        except:
            print(f'End in iteration {i}')
            more=False
    except:
        print(f'End in iteration {i}')
        more=False
        
driver.quit()
Full_links_DF=pd.DataFrame(Full_links)
Full_links_DF.to_csv("H:/2020-02/How to find a new home with Scraping and game theory/Codigo/Full_links.csv")
  
#----------------------------------------------------------------------------
#--------------------------------Read each apartment -----------------------------
#----------------------------------------------------------------------------
#Driver initilizer


options=webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument("--start-maximized")

data=pd.DataFrame()
i=0
Full_links_DF=pd.read_csv("H:/2020-02/How to find a new home with Scraping and game theory/Codigo/Full_links.csv")['0']
for url_tem in Full_links_DF:
    try:
        #Open driver
        driver= webdriver.Chrome(executable_path=r'H:/2020-02/How to find a new home with Scraping and game theory/chromedriver.exe',options=options)
        print(f'Leyendo url {i} de {len(Full_links_DF)}')
        driver.get(url_tem)
        smart_delay(driver,30,'.//div[@class="m_property_info_table"]')
        #Elements
        Chara_url_temp=dict()
        get_information(driver,Chara_url_temp)
        Chara_url_temp.update({'URL':[url_tem]})
        
        data_tem=pd.DataFrame.from_dict(Chara_url_temp)
        data=data.append(data_tem)
        print(data_tem)
    except:
          print(f'Error no previsto en  url {i} de {len(Lista_Urls)}')
    print(f'Termino url {i} de {len(Lista_Urls)}')
    i=i+1
    driver.quit()
data.to_csv("H:/2020-02/How to find a new home with Scraping and game theory/Codigo/Data_Apartments.csv")


