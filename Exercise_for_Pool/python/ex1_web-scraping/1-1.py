import time
import requests
from bs4 import BeautifulSoup 
import re
import pandas as pd

class Restaurant:
    def __init__(self, name, tel, email, prefecture, city, banchi, building, url, ssl_):
        self.na = name
        self.te = tel
        self.em = email
        self.pr = prefecture
        self.ci = city
        self.ba = banchi
        self.bu = building
        self.ur = url
        self.ss = ssl_
    


url_1 = 'https://r.gnavi.co.jp/area/jp/japanese/rs/?bdgMax=500&coupon=REGULAR%2CRESERVE&plan=COURSE_RESERVE&point=SAVE%2CUSE'
url_2 = "https://r.gnavi.co.jp/area/jp/japanese/rs/?bdgMax=500&coupon=REGULAR%2CRESERVE&plan=COURSE_RESERVE&point=SAVE%2CUSE&p=2"

urls = [url_1, url_2]

inf_urls = []
restaurants_list = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

count = 0

for url in urls:

    res = requests.get(url, headers = headers)
    res.encoding = res.apparent_encoding
    time.sleep(3)
    soup = BeautifulSoup(res.text, 'html.parser')

    restaurants = soup.find_all('div',attrs={'class': 'style_restaurant__SeIVn'})

    for restaurant in restaurants:
        if restaurant.find('span', class_ = 'style_pr__vEk6c'):
            continue
        
        else:            
            get_a = restaurant.find('a')
            inf_urls.append(get_a.get('href'))
                        
            count += 1
        
        if count >= 50:
            break



for inf_url in inf_urls:
    res = requests.get(inf_url)
    time.sleep(3)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text,'html.parser')
    
    name = soup.find('h1',class_='shop-info__name').text
    tel = soup.find('span', class_='number').text
    email = ''
    
    address = soup.find('span', class_='region').text
    
    #都道府県
    pref_pattern = r'^(東京都|北海道|(?:京都|大阪)府|.{2,3}県)'
    pref_match = re.match(pref_pattern, address)
    prefecture = pref_match.group(0) if pref_match else ''
    
    rest = address[len(prefecture):]

    # 市区町村
    city_pattern = r'^([\u4E00-\u9FFF|あ-ん|ア-ン|0-9]+[市区町村条])+[\u4E00-\u9FFF]+'
    city_match = re.match(city_pattern, rest)
    city = city_match.group(0) if city_match else ''
    
    rest = rest[len(city):] if city else rest

    # 番地
    banchi_pattern = r'^[0-9]+(-[0-9]+){0,2}'
    banchi_match = re.match(banchi_pattern, rest)
    banchi = banchi_match.group(0) if banchi_match else ''
    
    rest = rest[len(banchi):] if banchi else rest

    # 建物名
    building = rest if rest else ''

    url = ''
    
    ssl_ = '' 
    
    restaurant = Restaurant(name,tel,email,prefecture,city,banchi,building,url,ssl_)
    
    restaurants_list.append(restaurant)




df = pd.DataFrame({
    '店舗名':[r.na for r in restaurants_list],
    '電話番号':[r.te for r in restaurants_list],
    'メールアドレス':[r.em for r in restaurants_list],
    '都道府県':[r.pr for r in restaurants_list],
    '市区町村':[r.ci for r in restaurants_list],
    '番地':[r.ba for r in restaurants_list],
    '建物名':[r.bu for r in restaurants_list],
    'URL':[r.ur for r in restaurants_list],
    'SSL':[r.ss for r in restaurants_list]
})

df.to_csv('1-1.csv',index=False,encoding='utf-8-sig')

