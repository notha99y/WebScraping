'''
Script that scrap the 'http://codedemos.com/sampleblog/' blog and output a .csv containing the headers
Title, url, date for the respective blog posts
'''

def main():
    import requests
    import os
    from bs4 import BeautifulSoup
    from csv import writer
    from utils import make_dir

    url = 'http://codedemos.com/sampleblog/'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    posts = soup.find_all(class_ = 'post-preview')
    # print(posts)

    save_path = os.path.join(os.getcwd(), 'data','scraped_data', 'blog')
    make_dir(save_path)

    with open(os.path.join(save_path, 'posts.csv'),'w') as csv_file:
        csv_writer = writer(csv_file)
        headers = ['Title', 'Link', 'Date']
        csv_writer.writerow(headers)

        for post in posts:
            title = post.find(class_ = 'post-title').get_text().replace('\n', '')
            # print(title)
            link = post.find('a')['href']
            # print(title, link)
            date = post.select('.post-date')[0].get_text()
            # print(title, link, date)
            csv_writer.writerow([title, link, date])

if __name__ =='__main__':
    main()
