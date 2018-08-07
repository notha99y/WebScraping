'''
Script that scraps http://www.fabpedigree.com/james/mathmen.htm for famous mathematicians

Tutorial from: https://realpython.com/python-web-scraping-practical-introduction/
'''
import os
from requests import get
from requests.exceptions import RequestException
from contextlib import closing # ensures that any network resources are freed when they go out of scope in that with block
from bs4 import BeautifulSoup
from csv import writer
from utils import make_dir
import time


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def get_names():
    '''
    Downloads the page where the list of mathematicians
    and returns their names
    '''
    url = 'http://www.fabpedigree.com/james/mathmen.htm'
    response = simple_get(url)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')

        names = set()  # build an unordered set of unique elements
        for li in html.select('li'):
            for name in li.text.split('\n'):
                if len(name) != 0:
                    # removes spaces before and after words
                    names.add(name.strip())
        return list(names)

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(url))


def get_hits_on_name(name):
    """
    Accepts a `name` of a mathematician and returns the number
    of hits that mathematician's Wikipedia page received in the
    last 60 days, as an `int`

    example page: https://xtools.wmflabs.org/articleinfo/en.wikipedia.org/Henri_Poincar%C3%A9
    """
    # url_root is a template string that is used to build a URL.
    url_root = 'https://xtools.wmflabs.org/articleinfo/en.wikipedia.org/{}'
    response = simple_get(url_root.format(name))

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')

        hit_link = [a for a in html.select('a')
                    if a['href'].find('latest-60') > -1]

        if len(hit_link) > 0:
            # Strip commas
            link_text = hit_link[0].text.replace(',', '')
            try:
                # Convert to integer
                return int(link_text)
            except BaseException:
                log_error("couldn't parse {} as an `int`".format(link_text))

    log_error('No pageviews found for {}'.format(name))
    return None


if __name__ == '__main__':
    # test
    # url = 'http://www.fabpedigree.com/james/mathmen.htm'
    # raw_html = simple_get(url)
    # html = BeautifulSoup(raw_html, 'html.parser')

    # for i, li in enumerate(html.select('li')):
    #     print(i, li.text)format

    print("Getting names")
    tic = time.time()
    names = get_names()
    print(
        "Done. Finished in {:.2f} secs. Total number of names found: {}".format(
            time.time() -
            tic,
        len(names)))

    results = []

    print("Getting hits")
    tic = time.time()
    for name in names:
        try:
            hits = get_hits_on_name(name)
            if hits is None:
                hits = -1
            results.append((hits, name))
        except BaseException:
            results.append((-1, name))
            log_error('Error encountered while processing '
                      '{}, skipping..'.format(name))

    print("Done. Finished in {:.2f}".format(time.time() - tic))

    results.sort(reverse=True)

    if len(results) > 5:
        top_marks = results[:5]
    else:
        top_marks = results

    print('\nThe most popular mathematicians are:\n')
    for (mark, mathematician) in top_marks:
        print('{} with {} pageviews'.format(mathematician, mark))

    no_results = len([res for res in results if res[0] == -1])
    print('\nBut we did not find results for '
          '{} mathematicians on the list'.format(no_results))

    print("===============")
    print("Saving results")
    tic = time.time()
    save_path = os.path.join(
        os.getcwd(),
        'data',
        'scraped_data',
        'mathematicians')
    make_dir(save_path)

    with open(os.path.join(save_path, 'mathematicians.csv'), 'w') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(['page views', 'name'])
        for rows in results:
            csv_writer.writerow([rows[0], rows[1]])

    print(
        "Done. Finished in {:.2f}. File saved in {}".format(
            time.time() - tic,
            save_path))
