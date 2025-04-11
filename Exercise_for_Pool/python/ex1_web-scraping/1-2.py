from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import ssl
import socket
import re

options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)


restaurants_inf_list = []

url = 'https://r.gnavi.co.jp/area/jp/japanese/rs/'

driver.get(url)
sleep(3)

def get_inf():
    links = driver.find_elements(By.CSS_SELECTOR, 'a.style_titleLink__oiHVJ')
    for link in links:
        href = link.get_attribute('href')
        restaurants_inf_list.append(href)
        if len(restaurants_inf_list) >= 50:
            return

get_inf()

button = driver.find_element(By.XPATH,('//*[@id="__next"]/div/div[2]/main/div[11]/nav/ul/li[4]/a'))
driver.execute_script('arguments[0].click();',button)

get_inf()

while len(restaurants_inf_list)<50:
    button = driver.find_element(By.XPATH,('//*[@id="__next"]/div/div[2]/main/div[11]/nav/ul/li[6]/a'))
    driver.execute_script('arguments[0].click();',button)
    get_inf()



restaurant_class_list = []
names = []
tel_nums = []
email_ads = []
prefectures = []
cities = []
banchi_list = []
buildings = []
urls = []
ssl_ = []


def check_ssl_certificate(hostname):
    port = 443  
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return True
    except:
        return False




for inf in restaurants_inf_list:
    driver.get(inf)
    sleep(3)

    name = driver.find_element(By.CSS_SELECTOR, '.shop-info__name').text
    names.append(name)
    
    
    tel = driver.find_element(By.CSS_SELECTOR, '.number').text
    tel_nums.append(tel)
    
    email = ''
    email_ads.append(email)

    address = driver.find_element(By.CSS_SELECTOR, '.region').text
    #都道府県
    pref_pattern = r'^(東京都|北海道|(?:京都|大阪)府|.{2,3}県)'
    pref_match = re.match(pref_pattern, address)
    prefecture = pref_match.group(0) if pref_match else ''
    prefectures.append(prefecture)
    
    rest = address[len(prefecture):]

    # 市区町村
    city_pattern = r'^[\u4E00-\u9FFF]+'
    city_match = re.match(city_pattern, rest)
    city = city_match.group(0) if city_match else ''
    cities.append(city)
    
    rest = rest[len(city):] if city else rest

    # 番地
    banchi_pattern = r'^[0-9]+(-[0-9]+){0,2}'
    banchi_match = re.match(banchi_pattern, rest)
    banchi = banchi_match.group(0) if banchi_match else ''
    banchi_list.append(banchi)
    
    rest = rest[len(banchi):] if banchi else rest

    # 建物名
    building = rest if rest else ''
    buildings.append(building)
    
    try:
        html = driver.find_element(By.CSS_SELECTOR, '.url.go-off')
        url = html.get_attribute('href')
    except:
        url = ''
    urls.append(url)
    
    ssl_.append(check_ssl_certificate(url))
    
driver.quit()


df = pd.DataFrame({
    '店舗名':names,
    '電話番号':tel_nums,
    'メールアドレス':email_ads,
    '都道府県':prefectures,
    '市区町村':cities,
    '番地':banchi_list,
    '建物名':buildings,
    'URL':urls,
    'SSL':ssl_
})

df.to_csv('1-2.csv',index=False,encoding='utf-8-sig')