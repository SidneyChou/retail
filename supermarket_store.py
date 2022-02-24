# -*- coding: utf-8 -*-
"""
crawler for supermarket store infomation
"""

import numpy as np
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re, datetime, csv
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--disable-popup-blocking")

driver = webdriver.Chrome(options = options)

listData = []
date = datetime.date.today()

def get_c4_hyper():
    url = "https://www.carrefour.com.tw/stores/"
    driver.get(url)
    sleep(5)
    select = driver.find_element_by_xpath('//*[@id="carrefour-tw-vulcan-block-store-list"]/div/div[2]/div/div/div[1]/div/div/div/div/ul/li[2]/a/span')
    driver.execute_script("arguments[0].click();", select)
    sleep(3)
    scroll()

    soup = bs(driver.page_source, "html.parser")
    
    for div in soup.select('div.card-storeInfo'):
        name = div.select_one('h5.h4.text-center').get_text()
        op_time = np.nan
        address = div.select_one('ul.traffic-info-list span').get_text()
        address = address.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
        address = re.sub(r"^[0-9]{3}\s", "", address)
        address = re.sub(r"^台", "臺", address)
        city = address[0:3]
        
        if "24h" in name:
            op_time = "24h"
        else:
            op_time = "non-24h"
        
        name = re.sub(r"24h", "", name)    
        
        listData.append({
            "brand": "Carrefour",
            "type": "Hypermarket",
            "name": name,
            "time": op_time,
            "address": address,
            "service": np.nan,
            "city": city,
            "record_date": date
        })


def get_c4_super():
    url = "https://www.carrefour.com.tw/stores/"
    driver.get(url)
    sleep(5)
    select = driver.find_element_by_xpath('//*[@id="carrefour-tw-vulcan-block-store-list"]/div/div[2]/div/div/div[1]/div/div/div/div/ul/li[3]/a/span')
    driver.execute_script("arguments[0].click();", select)
    sleep(3)
    scroll()

    soup = bs(driver.page_source, "html.parser")
    
    for div in soup.select('div.card-storeInfo'):
        name = div.select_one('h5.h4.text-center').get_text()
        op_time = np.nan
        address = div.select_one('ul.traffic-info-list span').get_text()
        address = address.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
        address = re.sub(r"^[0-9]{3}\s", "", address)
        address = re.sub(r"^台", "臺", address)
        city = address[0:3]
        
        if "24h" in name:
            op_time = "24h"
        else:
            op_time = "non-24h"
        
        name = re.sub(r"24h", "", name)    
        
        listData.append({
            "brand": "Carrefour",
            "type": "Supermarket",
            "name": name,
            "time": op_time,
            "address": address,
            "service": np.nan,
            "city": city,
            "record_date": date
        })
    
    
def get_pxmart():
    url = "https://www.pxmart.com.tw/#/shopList"
    driver.get(url)
    search = driver.find_element(By.CSS_SELECTOR, 'button.search-btn')
    driver.execute_script("arguments[0].click();", search)
    sleep(5)
    soup = bs(driver.page_source, "html.parser")
    
    for div in soup.select('div.search-result li'):
        name = div.select_one('div.intro div.name div.value').get_text()
        op_time = div.select_one('div.intro div.time div.value').get_text()
        address = div.select_one('div.address-info div.value').get_text()
        address = address.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
        address = re.sub(r"\([0-9]+\)", "", address)
        address = re.sub(r"(\.|。|、)[0-9]+", "", address)
        address = re.sub(r"^[0-9]+", "", address)
        address = re.sub(r"^台", "臺", address)
        # 修正店地址
        address = re.sub(r"^林市三和里三民東街359號1樓", "彰化縣員林市三民東街359號1樓", address) # 員林店
        address = re.sub(r"^鹿區中山路434號", "臺中市沙鹿區中山路434號", address) # 沙鹿中山
        city = address[0:3]
        service = []
        
        for item in div.select('div.services-info div.tag-list div.tag-item'):
            service.append(item.get_text())
        
        strService = ",".join(service)
       
        listData.append({
            "brand": "PX Mart",
            "type": "Supermarket",
            "name": name,
            "time": op_time,
            "address": address,
            "service": strService,
            "city": city,
            "record_date": date
        })
    
def get_simplemart():
    url = "https://www.simplemart.com.tw/ec99/ushop20097/map.asp"
    driver.get(url)
    search = driver.find_element(By.CSS_SELECTOR, 'div.map-search a')
    driver.execute_script("arguments[0].click();", search)
    
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div#plF>ul")
            )
        )

        for store in driver.find_elements(By.CSS_SELECTOR, "div#plF>ul"):
            name = store.find_element(By.CSS_SELECTOR, "li.map-name").get_attribute('innerText')
            op_time = store.find_element(By.CSS_SELECTOR, "li.map-time").get_attribute('innerText')
            op_time = re.sub(r"~", "-", op_time)
            address = store.find_element(By.CSS_SELECTOR, "li.map-add").get_attribute('innerText')
            address = address.translate(str.maketrans('０１２３４５６７８９','0123456789'))
            address = re.sub(r"^[0-9]+", "", address)
            address = re.sub(r"^台", "臺", address)
            address = re.sub(r"^桃園縣", "桃園市", address) 
            # 修正店地址
            address = re.sub(r"^天祥七街113號", "桃園市桃園區天祥七街113號", address) # 桃園天祥店
            address = re.sub(r"^彰化市泰和中街76號", "彰化縣彰化市泰和中街76號", address) # 彰化泰和店
            address = re.sub(r"^新德街198號", "桃園市平鎮區新德街198號", address) # 平鎮新德店
            address = re.sub(r"^萬美街一段65號", "臺北市文山區萬美街一段65號", address) # 文山萬美店
            address = re.sub(r"^重陽路一段43巷33號", "新北市三重區重陽路一段43巷33號", address) # 三重重陽二店
            city = address[0:3]
            
            try:
                service = store.find_element(By.CSS_SELECTOR, "li.map-button li.map-food img").get_attribute('title')
            except NoSuchElementException: 
                service = np.nan  
            
            listData.append({
                "brand": "Simple Mart",
                "type": "Supermarket",
                "name": name,
                "time": op_time,
                "address": address,
                "service": service,
                "city": city,
                "record_date": date
            })
    
    except TimeoutException:
        print("TimeoutException")

def write_csv():
    headers = ["brand","type","name","time","address", "service", "city","record_date"]
    with open('./data/supermarket.csv','w', encoding='utf-8', newline='') as f:
        write_csv = csv.DictWriter(f , headers)
        write_csv.writeheader()
        write_csv.writerows(listData)

def close():
    driver.quit()

def scroll():
    offset = 0 
    totalHeight = 0
    count = 0
    countLimit = 3
    
    while count <= countLimit:
        offset = driver.execute_script(
            'return window.document.documentElement.scrollHeight;'
        )

        js_code = f'''
            window.scrollTo({{
                top: {offset}, 
                behavior: 'smooth'
            }});
        '''
        
        driver.execute_script(js_code)
        sleep(2)
        
        totalHeight = driver.execute_script(
            'return window.document.documentElement.scrollHeight;'
        )
        
        if offset >= totalHeight:
            count += 1    
                                      
if __name__ == "__main__":
    get_c4_hyper()
    get_c4_super()
    get_pxmart()
    get_simplemart()
    write_csv()
    close()