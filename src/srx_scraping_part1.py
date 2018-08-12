'''
Script that scraps the PSF of resale homes near mrt lines (within 1 km)
Part 1: would not be able to get the prices due to some javascript.
Refer to Part 2.
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

    stations = soup.find('div', id='mrtGraph').div.find_all('div')
    for station in stations:
        station_name = station['class'][0]
        psf = station.text
        print("Station name: {}, PSF: ${}".format(station_name, psf))
