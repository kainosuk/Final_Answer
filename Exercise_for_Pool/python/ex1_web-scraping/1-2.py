from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re

options = Options()
options.headless = True

class Restaurant:
    def __init__(self, name, tel, email, prefecture, url):
        self.na = name
        self.te = tel
        self.em = email
        self.pr = prefecture
        self.ur = url

urls = [
    'https://r.gnavi.co.jp/area/jp/japanese/rs/?bdgMax=500&coupon=REGULAR%2CRESERVE&plan=COURSE_RESERVE&point=SAVE%2CUSE',
    'https://r.gnavi.co.jp/area/jp/japanese/rs/?bdgMax=500&coupon=REGULAR%2CRESERVE&plan=COURSE_RESERVE&point=SAVE%2CUSE&p=2'
]

restaurants_inf_list = []

driver = webdriver.Chrome(options=options)

for url in urls:
    driver.get(url)
    sleep(3)

    links = driver.find_elements(By.CSS_SELECTOR, 'a.style_titleLink__oiHVJ')
    
    for link in links:
        href = link.get_attribute('href')
        if href:
            restaurants_inf_list.append(href)
        if len(restaurants_inf_list) >= 50:
            break

    if len(restaurants_inf_list) >= 50:
        break

restaurant_list = []

for inf in restaurants_inf_list:
    driver.get(inf)
    sleep(3)

    name = driver.find_element(By.CSS_SELECTOR, '.shop-info__name').text
    
    tel = driver.find_element(By.CSS_SELECTOR, '.number').text

    email = ''

    address = driver.find_element(By.CSS_SELECTOR, '.region').text
    pattern_pr = '東京都|北海道|(京都|大阪)府|.{2,3}県'
    mobj = re.search(pattern_pr, address)
    prefecture = mobj.group() if mobj else '不明'

    try:
        html = driver.find_element(By.CSS_SELECTOR, '.url.go-off')
        url = html.get_attribute('href')
    except:
        url = ''  
    restaurant = Restaurant(name,tel,email,prefecture,url)
    restaurant_list.append(restaurant)
driver.quit()


df = pd.DataFrame({
    '店舗名':[r.na for r in restaurant_list],
    '電話番号':[r.te for r in restaurant_list],
    'メールアドレス':[r.em for r in restaurant_list],
    '都道府県':[r.pr for r in restaurant_list],
    'URL':[r.ur for r in restaurant_list]
})

df.to_csv('1-2.csv',index=False,encoding='utf-8-sig')