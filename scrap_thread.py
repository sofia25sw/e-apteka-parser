import requests
import json
from bs4 import BeautifulSoup
import re
import threading
from math import ceil
from desc import process_desc

NO_IMAGE = 'http://e-apteka.md/files/products/nofoto.200x200.jpg?d3d1715a5cd51c4c9abd358a69c98868'
lock = threading.RLock()
counter = 1


def scrap(item_urls: list, fp, l):
    global counter
    for item_url in item_urls:
        item_url = item_url.strip()[1:-1]
        page = requests.get(item_url)
        # with open("page.html", 'wb') as f:
        #     f.write(page.content)
        soup = BeautifulSoup(page.text, 'html.parser')

        # Наименование
        name = soup.find('div', id='content').find('h2').text
        name = re.sub(r'\s+', ' ', name)

        # Производитель
        specs = soup.find('div', {'class': 'product'}).findAll('div')[1].text
        # print(specs)
        man_reg = r'Производитель:\s*(.+)'
        man = re.search(man_reg, specs)
        if man is None:
            man = 'Производитель не указан'
        else:
            man = man.group(1)
            man = re.sub(r'\s+', ' ', man)

        # Срок годности
        expire_date_reg = r'(\d\d\.){2}\d+'
        expire_date = re.search(expire_date_reg, specs)
        if expire_date is None:
            expire_date = 'Нет срока годности'
        else:
            expire_date = expire_date.group(0)

        # Цена/наличие
        price_reg = r'Цена:(.+)'
        price = re.search(price_reg, specs)
        if price is None:
            price = 'Нет в наличии'
        else:
            price = price.group(1)

        # Ссылка на картинку
        image_link = soup.find('div', {'class': 'product'}).find('img')['src']
        if image_link == NO_IMAGE:
            image_link = None

        # Категория
        categ = soup.find('div', id='path').findAll('a')[1:]
        categ = list(map(lambda a: a.text, categ))
        categ = ' -> '.join(categ)


        # Описание товара
        desc = soup.find('div', {'class': 'description'}).contents
        desc = process_desc(desc)

        res = {
            'Name': name,
            'Manufacturer': man,
            'Expire date': expire_date,
            'Price': price,
            'Image link': image_link,
            'Category': categ,
            'Description': desc,
            'URL': item_url

        }

        res = json.dumps(res, ensure_ascii=False)

        lock.acquire()
        fp.write(res + '\n')
        print(f'{counter}/{l}')
        counter += 1
        lock.release()


if __name__ == '__main__':
    with open('items.json', 'r', encoding='utf-8') as source, open('res.txt', 'w', encoding='utf-8') as fp:
        source = list(source)

        threads = []
        bunch = ceil(len(source) / 15)
        l = len(source)
        for t in range(15):
            threads.append(threading.Thread(target=scrap, args=[source[t * bunch:(t + 1) * bunch], fp, l]))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # i = 1
        # for url in source:
        #     scrap(url.strip()[1:-1], fp)
        #     print(f'{i}/{l}')
        #     i += 1
        #     scrap('http://e-apteka.md/products/Aspirin_Kardio_tab_100mg_20', fp)
