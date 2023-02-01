import requests
import bs4
from bs4 import BeautifulSoup

def collect_page_values(cost, name):
    page = requests.get('https://www.ohiolottery.com/Games/ScratchOffs/$' + cost + '-Games/' + name)

    soup = BeautifulSoup(page.content, 'html5lib')

    values = []
    table = soup.find('div', attrs = {'class': 'tbl_PrizesRemaining'}, recursive=True)
    for row in table.findAll('td', recursive=True):
        if row.text != '\xa0':
            values.append(row.text.strip('$ '))

