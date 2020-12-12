import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://ifoodie.tw/explore/'

paras_1 = {'':'台北市'}
paras_2 = {'':'餐酒館/酒吧'}
s = f'{urlencode(paras_1)}/list/{urlencode(paras_2)}'.replace('=', '')

r = requests.get('https://ifoodie.tw/explore/%E5%8F%B0%E5%8C%97%E5%B8%82/list/%E9%A4%90%E9%85%92%E9%A4%A8%2F%E9%85%92%E5%90%A7')
soup = BeautifulSoup(r.text, 'html.parser')

# print(soup.prettify)
# 營業時間、平均消費額

# link = soup.find('a',{'class':'jsx-2133253768 title-text'})
# a_tags = soup.find_all('a',{'class':'jsx-2133253768 title-text'})
# for tag in a_tags:
#     print(tag.get('href'))
# print(link)

dct = {'name':[], 'address':[], 'avg_price':[], 'link':[]} # 店名、地址相同屬性可merge # 均價部分把「均價」文字去掉只留下價格 #營業時間需點進link，先存link進字典

for name, address, avg_price, link in zip(soup.find_all('a', {'class':'jsx-2133253768 title-text'}), soup.find_all('div', {'class':'jsx-2133253768 address-row'}), soup.find_all('div', {'class':'jsx-2133253768 avg-price'}), soup.find_all('a', {'class':'jsx-2133253768 title-text'})):
    dct['name'].append(name.text)
    dct['address'].append(address.text)
    dct['avg_price'].append(list(avg_price)[2])
    dct['link'].append(f'https://ifoodie.tw{link.get("href")}')

df = pd.DataFrame(dct)

print(df)