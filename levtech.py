# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random

print("レバテックのurlを入力してください")

target = input(">")

print('')

print("取得数の入力（数字）")

num = int(input(">"))

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "levtech-"
path = dir + file_name + datetime + '.csv'

if target == "test":
    target = "https://career.levtech.jp/engineer/offer/search/?keyword=+Laravel"

    path = dir + file_name + 'test.csv'

response = requests.get(target)

base_url = "https://career.levtech.jp/"
company = []

try:
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(random.randint(1, 10))
        new_company = soup.find_all('span', class_='companyName')

        company += new_company
        company = list(set(company))
        count = len(company)

        print(count)

        next = soup.select('body > div.page > div > div.l-column.x-clearFix > div.l-searchMain > ul.pagination.x-clearFix > li.pagination__list.pagination__list--next > span > a')
        next_url = next[0].attrs['href']

        if count >= num:
            break

        dynamic_url = urljoin(base_url, next_url)
        print(dynamic_url)
        response = requests.get(dynamic_url)

    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + '\n')
        for item in company:
            f.write(item.get_text() + ',' + '\n')
        f.write(dynamic_url)

except:
    print('AccessError')
    print('次のurl:' + dynamic_url)
    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + '\n')
        for item in company:
            f.write(item.get_text() + ',' + '\n')
        f.write(dynamic_url)
