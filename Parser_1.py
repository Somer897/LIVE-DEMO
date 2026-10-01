from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium import webdriver

driver=webdriver.Chrome()

driver.get("https://catalog.onliner.by/mobile")

def get_all_links_on_page():
    elements = driver.find_elements(By.CLASS_NAME, value='catalog-form__link')

    ads_list = []
    for element in elements:
        ads_list.append(element.get_attribute('href'))


    return ads_list

def click_next_page():
    clickable_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div[4]/div/div/div/div/div[3]/div[3]/a'))
    )

    clickable_element.click()


def clean_links(links: list):
    clear_links = []
    very_clear_links = []

    for item in links:
        if item == None or 'forum.' in item or 'tech.' in item:
            pass
        else:
            clear_links.append(item)

    for item in clear_links:
        if 'prices' in item or 'reviews' in item or 'used' in item:
            pass
        else:
            very_clear_links.append(item)

    return very_clear_links

links_list = []
try:
    for iter in range(0, 5, 1):
        links_list += get_all_links_on_page()
        time.sleep(2)
        click_next_page()
except:
    print('error')
finally:
    print("All done")
    clean_links_list = clean_links(links_list)

with open('main.txt', 'a', encoding='UTF-8') as file:
     file.write('\n'.join(map(str, clean_links_list)))

table = pd.DataFrame()
for link in clean_links_list:
    driver.get(link)

    lists = []
    lists.append({'Название модели:': driver.find_element(By.CLASS_NAME, value= 'catalog-masthead__title').text})
    elements = driver.find_elements(By.CSS_SELECTOR, value = '.product-specs__table tr')
    for item in elements:
            
        tds = item.find_elements(By.TAG_NAME, value='td')
        if len(tds) == 2:
            if not tds[1].text:
                if tds[1].find_elements(By.CLASS_NAME, value='i-x'):
                    lists.append({tds[0].text: 'no'})
                else:
                    lists.append({tds[0].text: 'yea'})
            else:
                lists.append({tds[0].text: tds[1].text})



    # new_row = pd.DataFrame([lists])
    # table = pd.concat([table, new_row], ignore_index=True)

    whatever = 0
    for i in range(table.shape[0]):
        if str(table[115][i]) != 'nan':
            whatever = i

    table.loc[whatever]
    abc = []
    for d in table.loc[whatever]:
        for key, _ in d.items():
            abc.append(key)

    tab = pd.DataFrame(columns=abc)
    for i in range(table.shape[0] - 1):
        for j in range(table.shape[1] - 1):
            for key, value in table[j][i]:
                if 
