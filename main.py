from selenium import webdriver
import os
import time
from bs4 import BeautifulSoup as bs
import json

keywords=['mobile shops', 'tea shops']
locations=['la', 'new york']

max_data_keyword_per_location = 100

for location in locations:
    for keyword in keywords:
        url=f"https://www.google.com/search?hl=en&tbm=lcl&q={keyword.replace(' ', '+')}+in+{location.replace(' ', '+')}&oq={keyword.replace(' ', '+')}+in+{location.replace(' ', '+')}"

        wcr_dict = os.getcwd() + '//chromedriver.exe'
        driver = webdriver.Chrome(executable_path=wcr_dict)

        driver.get(url)
        while max_data_keyword_per_location > 0:
            
            time.sleep(5)
            
            store_name = driver.find_elements_by_css_selector('.cXedhc.uQ4NLd')
            for x in range(0, len(store_name)-1):
                a=store_name[x].get_attribute('innerHTML')
                soup = bs(a, 'html.parser')
                data_s=soup.get_text(separator='$').replace('\n', '').replace('  ', '').replace('   ', '').replace('$ ', '').replace('· ', '$').replace(' ⋅ ', '').replace('$Open', '$').replace('$$', '$').split('$')
                if len(data_s) > 5 and len(data_s) < 7:
                    name = data_s[0]
                    ratings= data_s[1]
                    number_ratings = data_s[2].replace('(', '').replace(')', '').replace(' ', '')
                    store_type = data_s[3]
                    address = data_s[4]
                    closes = data_s[5].replace('Closes', '').replace(' ', '')
                    try:
                        mobile_no = data_s[6].replace(' ', '')
                        dictionary ={ 
                                "store name" : name, 
                                "ratings" : ratings, 
                                "rated by" : number_ratings, 
                                "store type" : store_type,
                                "address" : address,
                                "closes" : closes,
                                "mobile no." : mobile_no
                        }
                        
                        json_object = json.dumps(dictionary, indent = 4) 
                        
                        with open(os.getcwd()+"//data.json", "a") as outfile: 
                            outfile.write(json_object) 
                    except:
                        dictionary ={ 
                                "store name" : name, 
                                "ratings" : ratings, 
                                "rated by" : number_ratings, 
                                "store type" : store_type,
                                "address" : address,
                                "closes" : closes,
                        }
                        
                        # Serializing json  
                        json_object = json.dumps(dictionary, indent = 4)
                        
                        # Writing to sample.json 
                        with open(os.getcwd()+"//data.json", "a") as outfile: 
                            outfile.write(json_object) 

            max_data_keyword_per_location-= 20
            if max_data_keyword_per_location > 0:
                try:
                    driver.find_element_by_id('pnnext').click()
                except:
                    break
            time.sleep(5)

        driver.quit()
