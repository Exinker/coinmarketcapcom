from datetime import datetime
import json
import os
import random
import time

import requests
from bs4 import BeautifulSoup


URL = 'https://coinmarketcap.com'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
}

def parse_page(url: str):

    def parse_name(tree: BeautifulSoup):
        try:
            if tree.find('a').find_all('p'):
                text = ', '.join([item.text for item in tree.find('a').find_all('p')])
            else:
                text = ', '.join([item.text for item in tree.find_all('span')][1:])
        except:
            text = 'FIXME'

        return text

    def parse_price(tree: BeautifulSoup):
        try:
            if tree.find('a'):
                text = tree.find('a').text
            else:
                text = tree.find('span').text
        except:
            text = 'FIXME'

        text = text[1:]
        text = text.replace(',', '')

        return text

    # send a request and get a response
    response = requests.get(
        url=url,
        headers=HEADERS,
    )

    # parse the response
    soup = BeautifulSoup(response.text, 'lxml')

    # parse page and scrape the data row by row
    data = []

    rows = soup.find('table').find('tbody').find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        datum = {
            'url': URL + columns[2].find('a').get('href'),
            'name': parse_name(columns[2]),
            'price': parse_price(columns[3]),
        }

        data.append(datum)

    return data

def parse_pages():

    # parse pages one by one until the last page
    data = []

    page = 1
    while True:
        try:
            data += parse_page(
                url=URL + f'/?page={page}'
            )  # add scraped data
            page += 1

            time.sleep(10 * random.random())  # sleep for couple of seconds

        except:
            break

    print(f'total amount of data: {len(data)}')

    return data

if __name__ == '__main__':

    # # parse and scrape data
    # data = parse_pages()

    # create folder to storage
    date = datetime.today().strftime('%Y-%m-%d')

    filedir = os.path.join('.', 'data', date)
    if not os.path.exists(filedir):
        os.makedirs(filedir)

    # # save scraped data to json file    
    # with open('data.json', 'w') as file:
    #     json.dump(data, file, indent=4)
