# Import packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


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

from db import DataBase
db = DataBase('../newsdata.sqlite')
conn = db.create_connection()


insert_record_sql = """ INSERT OR IGNORE INTO news (id, url) VALUES(?, ?)"""
        # Insert new record into table 
#Open web browsers
driver=webdriver.Chrome('D:/chromedriver')

driver.get('http://vneconomy.vn/')
stock_market_topic = driver.find_element_by_xpath('//*[@id="ActiveMenu6"]').click()

for i in range(100):
    sleep(10)
    urls = driver.find_elements_by_xpath('//*[@id="LoadTimeLine"]//a')
    next_button = driver.find_elements_by_xpath('//*[@class="more"]')
    
    if not next_button:
        urls[0].send_keys(Keys.END)        
        continue
    else:
        for u in urls:            
            url =  u.get_attribute('href') 
            id_key = int(hashlib.sha256(url.encode('utf-8')).hexdigest(), 16) % 10**8
            db.insert_table(conn, (id_key, url), insert_record_sql)
        next_button[0].click()
        sleep(10)

    


