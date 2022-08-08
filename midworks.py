# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random


def output(path, titles, fees):
    with open(path, 'w') as f:
        f.write('title' + ',' + 'link' + ',' + 'fee' + '\n')

        for (title, fee) in zip(titles, fees):

            # タイトル名
            title_text = title.text
            title_text = title_text.replace(' ', '')
            title_text = title_text.replace(',', '')

            # 案件のurl取得
            url = title.get('href')
            url = urljoin(base_url, url)

            # 給与の取得
            fee = fee.get_text()
            fee = fee.strip()
            fee = fee.replace(' ', '')
            fee_text = fee.replace(',', '')

            f.write(title_text + ',' + url + ',' + fee_text + ',' + '\n')

        f.write(dynamic_url)


print("Midworksのurlを入力してください")

target = input(">")

print('')

print("取得数の入力（数字）")

num = int(input(">"))

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "midworks-"
path = dir + file_name + datetime + '.csv'

if target == "test":
    target = "https://mid-works.com/projects?page=2&presco_sid=670.118.60.Q75wq7Z8o9526416&presco_sid=670.118.60.Q75wq7Z8o9526416"

    path = dir + file_name + 'test.csv'

response = requests.get(target)

titles = []
fees = []

base_url = "https://mid-works.com"
count = 0

try:
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 検索なしの場合(/project)
        title = soup.select('#project-list > div > a')
        fee = soup.select(
            '#project-list > div > div:nth-child(2) > div > div.row.mb-2 > div.col-sm-10')

        # 金額のみ
        # fee = soup.select(
        #     '#project-list > div > div:nth-child(2) > div > div.row.mb-2 > div.col-sm-10 > span')

        # 検索ありの場合(/skile)
        # title = soup.select(
        #     '#main > form > div > div > div.col-lg-8.mb-5 > div.mt-sm-4 > div.project-list> a')
        # fee = soup.select(
        #     '#main > form > div > div > div.col-lg-8.mb-5 > div.mt-sm-4 > div > div > div > div.row.mb-2 > div.col-sm-10')

        titles += title
        fees += fee

        next = soup.find('a', {"rel": 'next'})

        next_url = next.attrs['href']

        if count >= num:
            break

        count = len(titles)
        print(count)

        dynamic_url = urljoin(base_url, next_url)
        print(dynamic_url)
        response = requests.get(dynamic_url)

    # CSVファイルの出力
    output(path, titles, fees)

except:
    print('AccessError')
    print('次のurl:' + dynamic_url)

    # CSVファイルの出力
    output(path, titles, fees)
