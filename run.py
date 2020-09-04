import glob
import json
import html5lib
import requests
from bs4 import BeautifulSoup
import pandas as pd


session = requests.session()
def login():
    print('login...')
    datas = {
        'username': 'user',
        'password': 'user12345'
    }
    res = session.post('http://localhost:5000/login', data=datas)

    soup = BeautifulSoup(res.text, 'html5lib')

    page_item = soup.find_all('li', attrs={'class': 'page-item'})
    total_page = len(page_item) - 2
    return total_page


def get_urls(page):
    print('geting urls... page {}'.format(page))
    params = {
        'page': page
    }


    res = session.get('http://localhost:5000', params=params)

    soup = BeautifulSoup(res.text, 'html5lib')

    titles = soup.find_all('h4', attrs={'class': 'card-title'})
    urls = []
    for title in titles:
        url = title.find('a')['href']
        urls.append(url)


    return urls

def get_detail(url):
    print('geting detail... {}'.format(url))
    res = session.get(' http://localhost:5000'+url)


    soup = BeautifulSoup(res.text, 'html5lib')
    title = soup.find('title').text.strip()

    price = soup.find('h4', attrs={'class': 'card-price'}).text.strip()
    stock = soup.find('span', attrs={'class': 'card-stock'}).text.strip().replace('stock: ', '')
    category = soup.find('span', attrs={'class': 'card-category'}).text.strip().replace('category: ', '')
    description = soup.find('p', attrs={'class': 'card-text'}).text.strip().replace('Description: ', '')

    dict_data = {
        'title': title,
        'price': price,
        'stock': stock,
        'category': category,
        'description': description,
    }

    with open('./result/{}.json'.format(url.replace('/', '')), 'w') as outfile:
        json.dump(dict_data, outfile)



def create_csv():
    files = sorted(glob.glob('./result/*.json'))

    datas = []
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)
    df = pd.DataFrame(datas)
    df.to_csv('results.csv', index=False)


    print('csv generated...')

def run():
    total_pages = login()

    option = int(input('input option number:\n1.collecting all urls\n2.get detail all products\n3.create csv:\n '))
    if option == 1:
        total_urls = []
        for i in range(total_pages):
            page = i + 1
            urls = get_urls(page)
            total_urls += urls # total urls = total urls+urls
        with open('all_urls.json', 'w') as outfile:
            json.dump(total_urls, outfile)

    if option == 2:
        with open('all_urls.json') as json_file:
            all_url = json.load(json_file)

        for url in all_url:
            get_detail(url)

    if option == 3:
        create_csv()

if __name__ == '__main__':
    run()