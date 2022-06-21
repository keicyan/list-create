# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random

print("アイミツのurlを入力してください")

target = input(">")

print('')

print("取得数の入力（数字）")

num = int(input(">"))

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "aimitsu-"
path = dir + file_name + datetime + '.csv'

if target == "test":
    target = "https://imitsu.jp/ct-app-developer/bu-web-apps/"

    path = dir + file_name + 'test.csv'

response = requests.get(target)

base_url = "https://imitsu.jp/ct-app-developer/bu-web-apps/"
company = []

try:
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(random.randint(1, 10))

        # 元のやつ
        # new_company = soup.select(
        #     '#app > div.content > div > section.section-wrap > section.section-main > section.service-list > div.list-box > article > div.service-detail > div > div.service-detail-box > div.service-detail-inner > h3 > div > a')

        new_company = soup.find_all('span', class_='caption')

        company += new_company
        company = list(set(company))
        count = len(company)

        print(count)

        next = soup.select(
            '#app > div.content > div > section.section-wrap > section.section-main > section.service-list > nav > ul > li:nth-child(15) > a')
        next_url = next[0].attrs['href']

        if count >= num:
            break

        print(next_url)
        response = requests.get(next_url)

    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + 'url' + ',' + '\n')
        for item in company:
            get_text = item.text
            get_text = get_text.replace("出典：", "").strip()
            get_text = get_text.replace(" http", ",http")
            f.write(get_text + ',' + '\n')
        f.write(next_url)

except:
    print('AccessError')
    print('次のurl:' + next_url)
    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + '\n')
        for item in company:
            get_text = item.text
            get_text = get_text.replace("出典：", "").strip()
            get_text = get_text.replace(" http", ",http")
            f.write(get_text + ',' + '\n')
        f.write(next_url)
