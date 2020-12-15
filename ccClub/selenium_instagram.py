from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from urllib.parse import urlencode
from urllib.parse import quote
import string
import pandas as pd
import re

#讀資料 #這邊要請大家改成自己的資料路徑
data = pd.read_csv("/Users/hazel_lin/Documents/GitHub/ccClubFall2020/ccClub/1213_info.csv")
bar = data['name']

#做bar店名轉換list

bar_list = []
url = 'https://www.instagram.com/explore/tags/'

for i in range(len(bar)):
    s = data['name'][i]
    #去掉標點符號
    name = re.sub('[%s]' % re.escape(string.punctuation), '', s)
    lst = name.split()
    name = ''.join(lst)
    name = quote(name, safe = string.printable) 
    url_ig = url + name +'/'
    bar_list.append(url_ig)
# print(bar_list)

browser = webdriver.Chrome()


url = 'https://www.instagram.com/'  
browser.get(url)

#填入帳號與密碼
try:
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
except:
    print('error')

#網頁元素定位
username_input = browser.find_elements_by_name('username')[0]
password_input = browser.find_elements_by_name('password')[0]

#輸入帳號密碼
username_input.send_keys("searchforbarintaipei")
time.sleep(1)
password_input.send_keys("ccclub2020")

#登入
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH,
'//*[@id="loginForm"]/div/div[3]/button/div')))

#網頁元素定位
login_click = browser.find_elements_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')[0]

#點擊登入鍵
login_click.click()
time.sleep(random.uniform(1,5))

#不儲存登入資料
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')))

#網頁元素定位
store_click = browser.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')[0]

#點擊不儲存鍵
store_click.click()
time.sleep(random.uniform(1,5))

#不開啟通知
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[2]')))

#網頁元素定位                                                                                                    
notification_click = browser.find_elements_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')[0]

#點擊不開啟通知
notification_click.click()
time.sleep(random.uniform(1,5))

#開始讀整理好的url #先試試前面十個不然會跑超久
d = {}
n = 0
for url in bar_list[0:10]:
    browser.get(url)
    post_url = []
    soup = Soup(browser.page_source,"lxml")
    for elem in soup.select('div.KL4Bh img'): #抓出圖片的url
        if elem['src'] not in post_url:
            post_url.append(elem['src'])
    time.sleep(random.uniform(1,5))
        
    if post_url == []: #有的不知為什麼就是抓不出來那就跳過
        d[n] = []
        n += 1
    else:
        d[n] = post_url
        n += 1


p_url = pd.DataFrame.from_dict(d, orient='index')
 
print(p_url)

time.sleep(10)
browser.quit()