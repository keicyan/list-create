# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random

print("求人ボックスのurlを入力してください")

target = input(">")

print('')

print("取得数の入力（数字）")

num = int(input(">"))

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "joboffer-"
path = dir + file_name + datetime + '.csv'

if target == "test":
    target = "https://xn--pckua2a7gp15o89zb.com/%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2-laravel%E3%81%AE%E4%BB%95%E4%BA%8B"

    path = dir + file_name + 'test.csv'

response = requests.get(target)

base_url = "https://xn--pckua2a7gp15o89zb.com/"
company = []

try:
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(random.randint(1, 10))

        new_company = soup.find_all('p', class_='p-result_company')

        company += new_company
        company = list(set(company))
        count = len(company)

        print(count)

        next = soup.select(
            '#facetForm > div > div > article > nav > ul > li.p-paging_btn.p-paging_btn-next > a')
        next_url = next[0].attrs['href']

        if count >= num:
            break

        print(next_url)
        dynamic_url = urljoin(base_url, next_url)
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
