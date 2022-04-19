# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random

print("ゼロワンインターン のurlを入力してください")

target = input(">")

response = requests.get(target)

print('')

print("取得数の入力（数字）")

num = int(input(">"))

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "01intern-"
path = dir + file_name + datetime + '.csv'

base_url = "https://01intern.com/"
company = []

try:
    while True:
        soup = BeautifulSoup(response.content, 'html.parser')
        time.sleep(random.randint(1, 5))
        new_company = soup.find_all('h3', class_='i-job-suptitle')

        company += new_company
        company = list(set(company))
        count = len(company)

        print(count)

        next = soup.select('#app > div.l-contents > div.l-contents-l.l-job-flex > article > div.l-common-pagerArea.l-common-pagerArea_pc > ul > li:last-child > a')
        next_url = next[0].attrs['href']
        print(next_url)

        if count >= num:
            break

        # 次のページのurlの取得
        dynamic_url = urljoin(base_url, next_url)
        response = requests.get(dynamic_url)

    print('次のurl:' + dynamic_url)

    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + '\n')
        for item in company:
            text = item.get_text().strip()
            f.write(text + ',' + '\n')
        f.write(dynamic_url)

except:
    print('AccessError')
    print('次のurl:' + dynamic_url)
    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + '\n')
        for item in company:
            text = item.get_text().strip()
            f.write(text + ',' + '\n')
        f.write(dynamic_url)
