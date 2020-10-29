import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json
from time import sleep


# def get_pagination_limits():
#     start_url = 'http://e-apteka.md/spravka?keyword=%D0%90'
#     page = requests.get(start_url)
#     soup = BeautifulSoup(page.text, 'html.parser')
#
#     container = soup.select('a.other-page')
#     last_button = container[-1]
#     print(last_button)

def crawl():
    next_page = 'http://e-apteka.md/products'  # стартовая страница
    with open('items.json', 'w') as f:
        item_list = []
        while True:
            page = requests.get(next_page)
            soup = BeautifulSoup(page.text, 'html.parser')
            table = soup.find('table', {'class':'products'})
            trs = table.findAll('tr', {'class':'product'})
            # td_second = trs.find('')
            tds = list(map(lambda x: urljoin('http://e-apteka.md', x.findAll('td')[1].find('a')['href']), trs))
            item_list += tds

            for r in tds:
                f.write(json.dumps(r, ensure_ascii=False, indent=2) + '\n')

            try:
                next_page = soup.find('div', {'class':'pagination'}).find('a', {'class': 'selected'}).find_next_sibling('a')['href']
            except:
                return item_list
            next_page = urljoin('http://e-apteka.md', next_page)
            print(len(item_list))
            sleep(.3)













# def All_links():
#     all_page = 'http://e-apteka.md/products?page=all'
#     page = requests.get(all_page)
#     print(page.text)
#     soup = BeautifulSoup(page.text, 'html.parser')
#     print(all_page)
#     table = soup.find('table', {'class': 'products'})
#     trs = table.findAll('tr', {'class':'product'})
#     tds = list(map(lambda x: urljoin('http://e-apteka.md', x.findAll('td')[1].find('a')['href']), trs))
#
#     return tds


items = crawl()


# print(All_links())


# for i in range(1, 26):
#     response = requests.get(f'https://www.citilink.ru/catalog/mobile/smartfony/?available=1&status=55395790&p={i}').text
#     soup = BeautifulSoup(response, 'html.parser')
#
#     # print(i)
#
#     for el in soup.find_all('div', class_='subcategory-product-item'):
#         name = el.find('a', itemprop='name')['title']
#         print(name)
#         links = el.find('a', itemprop='name')['href']
#         print(links)
#         price = el.find('ins', class_='subcategory-product-item__price-num')
#         # print(price)
#         # price = str(price)
#         norm_price = re.sub("\D", "", str(price))
#         print("Цена:", norm_price)
#         # print([int(s) for s in str(price).split() if s.isdigit()])
#
# print(get_pagination_limits())


# for x in soup.find_all()
# price = el.find('div', itemprop='mame')[]

def get_object():
    pass

# Загружаем первую страницу
# Ищем ли, у которого класс селектед
# Ищем от этого след_стр
# Загружаем след стр, пока она существует
