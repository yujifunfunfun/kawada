import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import eel
import time
from logger import *
import csv
import re
import random
import pandas as pd
import numpy as np
import urllib.parse
from jan_to_asin import *

logger = set_logger(__name__)

def start_chrome():
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    ]
    UA = user_agent[random.randrange(0, len(user_agent), 1)]
    global option
    option = Options()                         
    option.add_argument('--lang=ja-JP')
    option.add_argument('--user-agent=' + UA)
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    option.add_argument("window-size=1300,1000")
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)


def login():
    driver.get(f"https://ganguoroshi.jp/login.html")
    driver.find_element_by_id('LOGINID').send_keys('7733004')
    driver.find_element_by_id('PASSWORD').send_keys('tanisi1231')
    driver.find_element_by_xpath('//*[@id="main"]/form/div/input').click()



def fetch_kawada_data(keyword_list):
    start_chrome()
    login()
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_all_elements_located)
    for keyword in keyword_list:
        keyword = urllib.parse.quote(keyword)
        kawada_item_data = []
        for page in range(1,100):
            elem = len(driver.find_elements_by_class_name("itemname"))
            if elem != 0:
                driver.get(f"https://ganguoroshi.jp/item_list.html?request=page&next_page={page}&SEARCH_MAX_ROW_LIST=100&item_list_mode=1&keyword={keyword}&siborikomi_clear=1&sort_order=4&x=0&y=0")
                wait.until(EC.presence_of_all_elements_located)                
                jan_list = driver.find_elements_by_css_selector("div.text h3")
                name_list = driver.find_elements_by_class_name("itemname")
                price_list = driver.find_elements_by_css_selector("p.price span span")
                url_list = driver.find_elements_by_css_selector("p.itemname a")

                for jan,name,price_str,url in zip(jan_list,name_list,price_list,url_list):
                    p = r'(.*)円'  
                    price = re.search(p, price_str.text).group(1)
                    kawada_item_data.append([jan.text,name.text,price,url.get_attribute("href")])
            else:
                break

    kawada_item_data_rev2 = jan_to_asin(kawada_item_data,driver)


    driver.quit()
    return kawada_item_data_rev2


def main():
    fetch_kawada_data(['任天堂'])




if __name__ == "__main__":
    main()