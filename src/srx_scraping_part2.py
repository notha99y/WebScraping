'''
Using Selenium to get the psf
Continued from part 1

In part 1, we managed to get the mrt names from the pages
'''
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from bokeh.io import show, output_file
from bokeh.plotting import figure


def get_data(mrtline_choosen):
    url = 'https://www.srx.com.sg/mrt-home-prices/property-listings-near-' + \
        mrtline_choosen + '-line'

    DRIVER = os.path.join(os.getcwd(), 'seleniumdrivers', 'chromedriver')
    browser = webdriver.Chrome(DRIVER)

    browser.get(url)
    # print(browser.page_source)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    stations = soup.find('div', id='mrtGraph').div.find_all('div')

    rental_psf = dict()
    resale_psf = dict()
    for station in stations:
        station_name = station['class'][0].split('-')[0]
        price_type = station['id'].split('-')[-1]

        if price_type == 'resale':
            temp = station.text.split('$')[-1].split(',')
            # print('temp: ', temp)
            price = ''
            for i in temp:
                price += i
            resale_psf[station_name] = price

        elif price_type == 'rental':
            rental_psf[station_name] = float(station.text.split('$')[-1])

        else:
            print("Error. Price type is neither rental nor resale")
            print(price_type)
            print("PSF: ", station.text)

    return rental_psf, resale_psf

    # print("Station name: {}, {} PSF: ${}".format(
    #     station_name, price_type, psf))

    browser.quit()


def plot_data(psf_dict, price_type, mrtline_choosen):

    output_file(price_type + 'PSFnear' + mrtline_choosen + '.html')
    station_names = []
    psf = []

    for key, value in sorted(psf_dict.iteritems(), key=lambda (k, v): (v, k), reverse=True):
        station_names.append(key)
        psf.append(value)

    p = figure(x_range=station_names, plot_height=1000, plot_width=1600,
               title=price_type + "PSF near" + mrtline_choosen + "MRT")
    p.xaxis.major_label_text_font_size = "14pt"
    p.vbar(x=station_names, top=psf, width=0.5)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)


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

    rental_psf, resale_psf = get_data(mrtline_choosen)

    while True:
        print("Would you like to view [1]: rental or [2]: resale?")

        request_view = str(input("Please enter 1 or 2: "))

        if request_view == '1' or '2':
            break
        else:
            print("Invalid input: ", request_view)

    if request_view == '1':
        plot_data(rental_psf, 'rental', mrtline_choosen)
    elif request_view == '2':
        plot_data(resale_psf, 'resale', mrtline_choosen)

    else:
        print("error")
