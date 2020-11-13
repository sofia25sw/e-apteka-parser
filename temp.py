url = 'http://e-apteka.md/products/mg_30______________________________________________________________________Egis_Pharmaceuticals_Ve'
from requests import get
from bs4 import BeautifulSoup
from lxml.html import fromstring as fs

page = get(url).text
path = fs(page)
print(path.xpath('normalize-space(//h2[1]/text())'))
soup = BeautifulSoup(page)
divs = soup.find('h2', {'class': 'huita'}).findAll('div', id='2')
ass = []
for div in divs:
    ass.append(div.find('a').text)

path.xpath('//h2[@class="huita"]/div[@id=2]/a/@href')