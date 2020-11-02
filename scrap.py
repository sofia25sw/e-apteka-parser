import requests
import json
from bs4 import BeautifulSoup
import re

NO_IMAGE = 'http://e-apteka.md/files/products/nofoto.200x200.jpg?d3d1715a5cd51c4c9abd358a69c98868'

def scrap(item_url: str, fp):
    page = requests.get(item_url)
    # with open("page.html", 'wb') as f:
    #     f.write(page.content)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Наименование
    name = soup.find('div', id='content').find('h2').text
    print(name)

    # Производитель
    specs = soup.find('div', {'class': 'product'}).findAll('div')[1].text
    # print(specs)
    man_reg = r'Производитель:\s*(.+)'
    man = re.search(man_reg, specs)
    if man is None:
        man = 'Производитель не указан'
    else:
        man = man.group(1)
    print(man)
    # Срок годности
    expire_date_reg = r'(\d\d\.){2}\d+'
    expire_date = re.search(expire_date_reg, specs)
    if expire_date is None:
        expire_date = 'Нет срока годности'
    else:
        expire_date = expire_date.group(0)
    print(expire_date)
    # Цена/наличие
    price_reg = r'Цена:(.+)'
    price = re.search(price_reg, specs)
    if price is None:
        price = 'Нет в наличии'
    else:
        price = price.group(1)
    print(price)
    # Ссылка на картинку
    image_link = soup.find('div', {'class': 'product'}).find('img')['src']
    if image_link == NO_IMAGE:
        image_link = ' '
    print(image_link)
    # Категория
    # Описание товара


if __name__ == '__main__':
    with open('items.json', 'r') as source, open('res.txt', 'w') as fp:
        for url in list(source)[:2]:
            scrap(url.strip()[1:-1], fp)
            # scrap('http://e-apteka.md/products/Aspirin_Kardio_tab_100mg_20', fp)
