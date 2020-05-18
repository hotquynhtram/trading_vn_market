# Import packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions  


from parsel import Selector
from selenium.webdriver.support.ui import Select
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import os
import hashlib
import sys
sys.path.append('..')
#Connect to database

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

import logging


logger = logging.getLogger("ebay_consumer")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)



from db import DataBase
db = DataBase('../newsdata.sqlite')
conn = db.create_connection()


insert_record_sql = """ INSERT OR IGNORE INTO news (id, url) VALUES(?, ?)"""
        # Insert new record into table 
#Open web browsers
driver=webdriver.Chrome('D:/chromedriver')
get_url = 'https://vietstock.vn/tai-chinh.htm'
driver.get(get_url)

#Date time range
times = pd.date_range(start='01/01/2015', end='01/01/2020')
date_range = times.strftime('%d/%m/%Y')

#Main
for date_input in date_range:    
    date_seach = driver.find_element_by_xpath("//*[@placeholder='Xem theo ngày']")
    date_seach.send_keys(date_input)
    date_seach.send_keys(Keys.ENTER)
    sleep(4)
    urls = driver.find_elements_by_xpath('//*[@class="channel-title"]//a')
    for u in urls: 
        try:
            url =  u.get_attribute('href') 
            id_key = int(hashlib.sha256(url.encode('utf-8')).hexdigest(), 16) % 10**8
            db.insert_table(conn, (id_key, url), insert_record_sql)
        except exceptions.StaleElementReferenceException:
            print(u)
            pass 
    date_seach.clear()
    logger.info(f"Finish crawling for the date: {date_input}")
    sleep(1)



# stock_market_topic = driver.find_element_by_xpath('//*[@id="menu-thi-truong-chung-khoan"]').click()


# for i in range(0, 100000,1):
#     sleep(5)
#     urls = driver.find_elements_by_xpath('//*[@id="channel-container"]//a')
#     for u in urls:            
#         url =  u.get_attribute('href') 
#         id_key = int(hashlib.sha256(url.encode('utf-8')).hexdigest(), 16) % 10**8
#         db.insert_table(conn, (id_key, url), insert_record_sql)
# #     topics_xpath = '//*[@id="content-paging"]'

# #     WebDriverWait(driver, \
# #                   10).until(expected_conditions.visibility_of_element_located((By.XPATH, topics_xpath)))    
        
#     next_button = driver.find_element_by_link_text(str(i+2))
#     driver.execute_script("arguments[0].click();", next_button)

# #     next_button.click()
#     logger.info(f"Jump to next page: Page {i+2}")
    






