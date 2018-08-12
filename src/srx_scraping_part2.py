'''
Using Selenium to get the psf
Continued from part 1

In part 1, we managed to get the mrt names from the pages
'''

from requests import get
from bs4 import BeautifulSoup

if __name__ == '__main__':
    MRTLINE = ['east-west',
               'circle',
               'north-south',
               'north-east',
               'thomson',
               'downtown']

    print("Choose the MRT line you wish to investigae")
    for i, mrtline in enumerate(MRTLINE):
        print("[{}]: {}".format(i, mrtline))
    choosen = int(input("Choose from 0 to {}: ".format(len(MRTLINE) - 1)))
    mrtline_choosen = MRTLINE[choosen]

    url = 'https://www.srx.com.sg/mrt-home-prices/property-listings-near-' + \
        mrtline_choosen + '-line'

    res = get(url, timeout=5)
    soup = BeautifulSoup(res.text, 'lxml')
