from dotenv import load_dotenv
from logger import set_logger
load_dotenv() #環境変数のロード
from logger import set_logger
logger = set_logger(__name__)
from sp_api.api import Catalog
from sp_api.api import CatalogItems

from sp_api.base.marketplaces import Marketplaces
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import os
from time import sleep
import re
import pandas as pd


def start_chrome():
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    ]
    UA = user_agent[random.randrange(0, len(user_agent), 1)]
    global option
    option = Options()  
    option.add_argument('--lang=ja-JP')
    option.add_argument('--headless')
    option.add_argument('--user-agent=' + UA)
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    option.add_argument("window-size=1000,800")
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=option) 
    



def fetch_jan_asin(kawada_item_data,driver):
    wait = WebDriverWait(driver, 10)
    n = 100
    kawada_item_list_per_100 = [kawada_item_data[i:i + n] for i in range(0, len(kawada_item_data), n)]
    jan_asin_list = []
    for kawada_item_100 in kawada_item_list_per_100:
        jan_list = []
        for kawada_item in kawada_item_100:
            jan = kawada_item[0]
            jan_list.append(jan)
        jan_100 = ','.join(map(str,jan_list))
        driver.get("https://caju.jp/bulk/convert")
        element = wait.until(EC.visibility_of_all_elements_located)
        driver.execute_script(f'document.getElementById("bulkKeywords").value="{jan_100}"')
        driver.find_element_by_id('bulkSubmit').click()
        element2 = wait.until(EC.visibility_of_all_elements_located)

        for i,n in zip(range(3,202,2),range(2,201,2)):
            try:
                jan = driver.find_element_by_xpath(f'/html/body/div/div/div[5]/div[1]/div[{i}]/div/div[2]/span[2]').text
                asin = driver.find_element_by_xpath(f'/html/body/div/div/div[5]/div[1]/div[{i}]/div/div[2]/span[1]').text
                jan_asin_list.append([jan,asin])
            except Exception as e:
                pass
    
    return jan_asin_list

def match_jan_asin(kawada_item_data,jan_asin_list):
    for kawada_item in kawada_item_data:
        kawada_jan = kawada_item[0]
        for jan_asin in set(jan_asin_list):
            fetch_jan = jan_asin[0]
            if kawada_jan == fetch_jan:
                kawada_item.append(jan_asin[1])
                break
    return kawada_item_data

def jan_to_asin(kawada_item_data,driver):
    jan_asin_list = fetch_jan_asin(kawada_item_data,driver)
    kawada_item_data_rev2 = match_jan_asin(kawada_item_data,jan_asin_list)
    return kawada_item_data_rev2






if __name__ == "__main__":
    start_chrome()
    jan_to_asin([['B08L7MS18T','aaa'],['B07G4QQYP7','bbb'],['B09BJP7Q1R','ccc'],['B09CM5GQRP','ddd']])


