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

def extract_name(name):
    name = re.findall(r'-Games/.+', name)
    return name[0][7:]

def avg_value(dict):
    for i in dict:
        total = 0
        num = 0
        for j in range(0, len(dict[i]), 2):
            dict[i][j] = dict[i][j].replace(',', '')
            dict[i][j+1] = dict[i][j+1].replace(',', '')
            if dict[i][j].replace('.', '0').isdigit():
                total += float(dict[i][j]) * float(dict[i][j+1])
            else:
                total += float(input('value of ' + dict[i][j])) * float(dict[i][j+1])
            num += int(dict[i][j+1])
        print(i)
        print(' Average: ')
        print(total / num)
        print('\n')
                
names = collect_game_names()
dict = {}
for i in names:
    cost = extract_cost(i)
    if cost == '1':
        name = extract_name(i)
        values = collect_page_values(i)
        dict[name] = values

avg_value(dict)
