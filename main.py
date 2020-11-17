from selenium import webdriver
import os
import time
import json
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

keywords=['美容', '美发', '理发', '造型', '沙龙']#good
locations=['new york city']

max_data_keyword_per_location = 500 #cool

for location in locations:
    for keyword in keywords:
        max_data_keyword_per = max_data_keyword_per_location
        url=f"https://www.google.com/search?hl=en&tbm=lcl&q={keyword.replace(' ', '+')}+in+{location.replace(' ', '+')}&oq={keyword.replace(' ', '+')}+in+{location.replace(' ', '+')}"

        wcr_dict = os.getcwd() + '//chromedriver.exe'
        driver = webdriver.Chrome(executable_path=wcr_dict)

        driver.get(url)
        while max_data_keyword_per > 0:
            time.sleep(5)
            store_name = driver.find_elements_by_css_selector('.C8TUKc.hide-focus-ring.rllt__link.a-no-hover-decoration')
            for x in range(0, len(store_name)-1):
                try:
                    store_name[x].click()
                    try:
                        confirm = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, ".qrShPb.kno-ecr-pt.PZPZlf.mfMhoc.PPT5v span")))
                    finally:
                        pass
                    time.sleep(6)
                    name=driver.find_element_by_css_selector('.qrShPb.kno-ecr-pt.PZPZlf.mfMhoc.PPT5v span').text
                    dictionary ={ 
                            "store name" : name
                    }
                    try:
                        el=driver.find_elements_by_class_name('YhemCb')
                        dictionary["store type"]=el[len(el)-1].replace('"', '')
                    except:
                        pass
                    try:
                        dictionary["ratings"]=driver.find_element_by_css_selector('.Ob2kfd .Aq14fc').text
                        dictionary["rated by"]=driver.find_element_by_css_selector('.hqzQac span a span').text
                    except:
                        pass
                    
                    a=driver.find_element_by_class_name('h2yBfgNjGpc__inline-item-view').get_attribute('innerHTML')
                    soup = bs(a, 'html.parser')
                    for info in soup.findAll("div", {"class": "zloOqf PZPZlf"}):
                        dictionary[str(info.get_text()).split(": ")[0]]=str(info.get_text()).split(": ")[1]

                    json_object = json.dumps(dictionary, indent = 4) 
                    
                    with open(os.getcwd()+"//data.json", "a") as outfile: 
                        outfile.write(json_object) 
                except Exception as e:
                    print(e)
            
            max_data_keyword_per-= 20
            if max_data_keyword_per > 0:
                try:
                    driver.find_element_by_id('pnnext').click()
                except:
                    break
            time.sleep(5)

        driver.quit()
