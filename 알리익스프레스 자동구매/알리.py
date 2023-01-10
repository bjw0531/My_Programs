# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pyperclip
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
options.add_argument("--no-sandbox")
options.add_argument('window-size=1920x1080')
options.add_argument('lang=ko_KR')
options.add_argument(
    f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# 클릭
driver.find_element(
    By.XPATH, '//*[@id="placeorder_wrap__inner"]/div/div[2]/div[2]/div/div/div[2]/button').click()
