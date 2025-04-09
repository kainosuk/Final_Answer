import time
import requests
from bs4 import BeautifulSoup 
import re
import pandas as pd

class Restaurant:
    def __init__(self, name, tel, email, prefecture, url):
        self.na = name
        self.te = tel
        self.em = email
        self.pr = prefecture
        self.ur = url
    


url_1 = 'https://r.gnavi.co.jp/area/jp/japanese/rs/?bdgMax=500&coupon=REGULAR%2CRESERVE&plan=COURSE_RESERVE&point=SAVE%2CUSE'
url_2 = "https://r.gnavi.co.jp/area/jp/japanese/rs/?bdgMax=500&coupon=REGULAR%2CRESERVE&plan=COURSE_RESERVE&point=SAVE%2CUSE&p=2"

urls = [url_1, url_2]

inf_urls = []
restaurants_list = []


count = 0

for url in urls:

    res = requests.get(url)
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

            time.sleep(3)
                        
            count += 1
        
        if count >= 50:
            break



for inf_url in inf_urls:
    res = requests.get(inf_url)
    res.encoding = res.apparent_encoding
    time.sleep(3)
    soup = BeautifulSoup(res.text,'html.parser')
    
    name = soup.find('h1',class_='shop-info__name').text
    tel = soup.find('span', class_='number').text
    email = ''
    
    address = soup.find('span', class_='region').text
    
    pattern_pr = '東京都|北海道|(京都|大阪)府|.{2,3}県'
    mobj = re.match(pattern_pr,address)
    prefecture = mobj.group()

    url = '' 
    
    time.sleep(3)
    restaurant = Restaurant(name,tel,email,prefecture,url)
    
    restaurants_list.append(restaurant)




df = pd.DataFrame({
    '店舗名':[r.na for r in restaurants_list],
    '電話番号':[r.te for r in restaurants_list],
    'メールアドレス':[r.em for r in restaurants_list],
    '都道府県':[r.pr for r in restaurants_list],
    'URL':[r.ur for r in restaurants_list]
})

df.to_csv('1-1.csv',index=False,encoding='utf-8-sig')

