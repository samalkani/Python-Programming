from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd
import re

driver = webdriver.Firefox()

driver.get("https://twitter.com/Cdiscount")

sleep(5)

while True:

    # execute a javascript function
    height = driver.execute_script("return document.body.scrollHeight")
    print(height)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(5)

    new_height = driver.execute_script("return document.body.scrollHeight")

    if height == new_height:
        break

#a

driver.close()
