import requests
import bs4
from bs4 import BeautifulSoup
import re

def collect_page_values(name):
    page = requests.get('https://www.ohiolottery.com/' + name)

    soup = BeautifulSoup(page.content, 'html5lib')

    values = []
    table = soup.find('div', attrs = {'class': 'tbl_PrizesRemaining'}, recursive=True)
    for row in table.findAll('td', recursive=True):
        if row.text != '\xa0':
            values.append(row.text.strip('$ '))
        
    return values

def collect_game_names():
    page = requests.get('https://www.ohiolottery.com/Games/InstantGames')
    name_soup = BeautifulSoup(page.content, 'html5lib')
    
    names = []
    table = name_soup.findAll('div', attrs = {'class': 'list_wrap'}, recursive=True)
    for i in table:
        for ele in i.findAll('a', recursive=True):
            names.append(ele['href'])
    
    return names

def extract_cost(name):
    cost = re.findall(r'\d+', name[19: 23])
    return cost[0]

names = collect_game_names()
print(names)
dict = {}
for i in names:
    cost = extract_cost(i)
    values = collect_page_values(i)
    dict[cost] = values


