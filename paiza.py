# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random

print("paizaのurlを入力してください")

target = input(">")

print('')

print("取得数の入力（数字）")

num = int(input(">"))

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "paiza-"
path = dir + file_name + datetime + '.csv'

if target == "test":
    target = "https://paiza.jp/career/search/?c%5Bfree_word%5D=PHP&commit=%E6%A4%9C%E7%B4%A2"

    path = dir + file_name + 'test.csv'

response = requests.get(target)

base_url = "https://paiza.jp/"
company = []

try:
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(random.randint(1, 10))
        new_company = soup.find_all('h4', class_='c-job_offer-recruiter__name')
        
        for item in new_company:
            tag = item.contents[1]
            company.append(tag)

        company = list(set(company))
        count = len(company)

        print(count)

        next = soup.select('#pagebody > div.jobContents.clearfix > div.main > div.boxPickup > div.c-pager > ul > li:last-child > div > a')
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
