'''
Script that scraps the url https://www.tripadvisor.com.sg/Attraction_Review-g294264-d2439664-Reviews-Universal_Studios_Singapore-Sentosa_Island.html
Get user profiles from their reviews
'''

import requests
import os
from bs4 import BeautifulSoup
from csv import writer
from utils import make_dir

url = 'https://www.tripadvisor.com.sg/Attraction_Review-g294264-d2439664-Reviews-Universal_Studios_Singapore-Sentosa_Island.html'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.body)

save_path = os.path.join(os.getcwd(), 'data', 'scraped_data', 'tripadvisor')

if __name__ == '__main__':
    pass
