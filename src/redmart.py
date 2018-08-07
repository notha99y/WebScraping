'''
Script that scrap redmart

Business question:
https://blog.moneysmart.sg/shopping/online-grocery-shopping-in-singapore/
'''

import requests
import json
import time
import math
import click
import os

# filename = str(time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime()))
filename = "data"

VERSION = 'v1.6.0'
PAGESIZE = 100


def requestForProducts(val, page):
    r = requests.get(
        'https://api.redmart.com/{}/catalog/search?category={}&pageSize={}&page={}'.format(
            VERSION, val, PAGESIZE, page))
    data = json.loads(r.text)
    return data


@click.command()
@click.argument('output_filepath', type=click.Path(exists=True))
def main(output_filepath):
    startTime = time.time()

    r = requests.get(
        'https://api.redmart.com/{}/catalog/search?extent=0&depth=1'.format(VERSION)) # gives the category
    data = json.loads(r.text)  # similarily can use data = r.json()

    # uri = [x['uri'] for x in data['categories']]
    uriDict = {}
    for x in data['categories']:
        for y in x['children']:
            try:
                uriDict[x['uri']].append(y['uri'])
            except KeyError:
                uriDict[x['uri']] = [y['uri']]
    productsDict = {}
    for key in uriDict:
        for val in uriDict[key]:
            data = requestForProducts(val, 0)
            time.sleep(0.5)
            try:
                # print('[Category]', str(val), 'Total', data['total'], 'Page', data['page'], 'Page Size', data['page_size'])
                print('[Category]', str(val), '[Total items]', data['total'])
            except KeyError:
                continue
            else:
                pass
            if data['total'] <= 100:
                # print(data['products'][0]['title'])
                for product in data['products']:
                    productsDict[product['title']] = product
            else:
                pages = math.ceil(data['total'] / PAGESIZE)
                for page in range(pages):
                    try:
                        data = requestForProducts(val, page)
                        # print(data['products'][0]['title'])
                        for product in data['products']:
                            productsDict[product['title']] = product
                    except KeyError:
                        pass
        print(len(productsDict))
        # print("./data/raw/{}.txt".format(filename))
        with open('./data/raw/{}.json'.format(filename), 'w+') as fp:
            try:
                existingProductsDict = json.load(fp)
                existingProductsDict.update(productsDict)
                json.dump(productsDict, fp)
            except BaseException:
                json.dump(productsDict, fp)

    print("Time taken to run:", str(time.time() - startTime))


if __name__ == '__main__':
    main()
