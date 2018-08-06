'''
This script would show the basics of using BeautifulSoup

documentations: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
video_ref: https://www.youtube.com/watch?v=4UcqECQe5Kc&t=564s
testing_url: http://codedemos.com/sampleblog/ (if you have wget on bash, you can wget the index.html)

credit: Traversy Media
'''

from bs4 import BeautifulSoup
import os

data_path = os.path.join(os.getcwd(), 'raw', 'data')
html_doc = open(os.path.join(data_path, os.listdir(data_path)[0]), 'r')

soup = BeautifulSoup(html_doc, 'html.parser')

'''
Direct Method
'''
# print(soup.body)
# print(soup.head)
# print(soup.head.title)

'''
find()/ find_all()

Usually you wont be using direct methods
You would use the find/ findall methods
'''
# el = soup.find('div')
# el = soup.find_all('div')
# el = soup.find(id='section-1')
# el = soup.find(class_ = 'navbar-nav ml-auto')
# el = soup.find(attrs = {"data-hello": "hi"})

'''
select()

We also have select
Select allows us to select things by css selectors which is very similar to jquery
'''
# el = soup.select('#section-1')
# el = soup.select('.nav-item')


'''
get_text()

Usually we just want the text inside the tags
'''

# el = soup.find(class_ = 'navbar-nav ml-auto').get_text()

# for item in soup.select('.nav-item'):
#     print(item.get_text())


'''
Navigation
'''

# el = soup.body.contents[7].contents[1].find_next_sibling()
# el = soup.find(class_ = 'navbar-nav ml-auto').find_previous_sibling()
# el = soup.find(class_ = 'nav-item').find_parent()
el = soup.find_all('p')
print(el)
