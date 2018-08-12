import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH_TO_DRIVER = os.path.join(os.getcwd(), 'seleniumdrivers', 'chromedriver')
browser = webdriver.Chrome(PATH_TO_DRIVER)

url = 'https://www.seleniumhq.org/'

browser.get('https://www.seleniumhq.org/')

elem = browser.find_element_by_link_text('Download')
print(elem)
print(elem.text)
print(elem.get_attribute('href'))
# elem.click()

searchBar = browser.find_element_by_id('q')
searchBar.send_keys('Download')
searchBar.send_keys(Keys.ENTER)
