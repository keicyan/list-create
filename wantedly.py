# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random

print("wontedly のurlを入力してください")

target = input(">")

if target == "test":
    target = "https://www.wantedly.com/projects?type=mixed&page=1&keywords%5B%5D=Vue.js"

print('')

print("取得数の入力（数字）")

num = int(input(">"))

response = requests.get(target)

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "wantedly-"
path = dir + file_name + datetime + '.csv'
# path = './data/sample.csv'

base_url = "https://www.wantedly.com/"
company = []
base_count = 0
same_count = 0

try:
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(random.randint(1, 5))
        new_company = soup.find_all('div', class_='company-name')

        for i in new_company:
            if len(i.contents) != 0:
                tag = i.a
                item = tag.text
                company.append(item)

        company = list(set(company))
        count = len(company)

        print(count)

        next = soup.find('a', attrs={'rel': 'next'})
        print(next.get("href"))

        if count == base_count:
            same_count += 1

        if same_count == 100:
            break

        if count >= num:
            break

        # 次のページのurlの取得
        dynamic_url = urljoin(base_url, next.get("href"))
        response = requests.get(dynamic_url)

        base_count = count

    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + '\n')
        for item in company:
            f.write(item + ',' + '\n')
        f.write(dynamic_url)

except:
    print('AccessError')
    print('次のurl:' + dynamic_url)
    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + '\n')
        for item in company:
            f.write(item + ',' + '\n')
        f.write(dynamic_url)
