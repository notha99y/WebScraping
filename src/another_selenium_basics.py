'''

find elements: https://selenium-python.readthedocs.io/locating-elements.html
'''


import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


DRIVER = os.path.join(os.getcwd(), 'seleniumdrivers', 'chromedriver')
url = 'https://www.google.com/'

browser = webdriver.Chrome(DRIVER)
browser.get(url)
searchBar = browser.find_element_by_id('lst-ib')
# searchBar.send_keys('Cool places to visit in Meteora')
searchBar.send_keys("Best places to have chocolates in Singapore")
time.sleep(1)
searchBar.send_keys(Keys.ENTER)

elem = browser.find_element_by_class_name("r")
print(elem)
print(elem.text)
print(elem.get_attribute('href'))
elem.click()
