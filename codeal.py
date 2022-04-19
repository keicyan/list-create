# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random

print("codealのurlを入力してください")

target = input(">")

print('')

print("取得数の入力（数字）")

num = int(input(">"))

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "codeal-"
path = dir + file_name + datetime + '.csv'

if target == "test":
    target = "https://www.codeal.work/jobs?skills=JavaScript,PHP,Vue.js,%20Laravel&categories=15-1199.00&area_with_full_remote=true&exclude_full_time=true&is_application_allowed=true&sort=random_rank_desc"

    path = dir + file_name + 'test.csv'

response = requests.get(target)

base_url = "https://www.codeal.work/"
company = []

try:
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(random.randint(1, 10))
        new_company = soup.find_all('span', class_='label')

        company += new_company
        company = list(set(company))
        count = len(company)

        print(count)

        next = soup.select('#app > div:nth-child(3) > div > div > div.col-12.col-lg-9.main > div.text-center.mt-c40 > div > ul > li.next > a')
        next_url = next[0].attrs['href']

        if count >= num:
            break

        # 次のページのurlの取得
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
