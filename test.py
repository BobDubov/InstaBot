import requests
from bs4 import BeautifulSoup
import datetime
import time

req = requests.get('https://ya.ru/')
soup = BeautifulSoup(req.text, 'lxml')

if soup.find('input', attrs={'id': 'text'}) == None:
    print(5)
else:
    print(soup.find('input', attrs={'id': 'text'}))
    print(soup.find('input', attrs={'id': 'text'}).get_attribute_list('aria-label'))