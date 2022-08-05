# coding: UTF-8
from optparse import TitledHelpFormatter
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random
import re

print("フリー情報収集用")

# target = input(">")
target = 'https://busiconet.co.jp/evowork/recommend-freelance-agent/'

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "free"
path = dir + file_name + datetime + '.csv'

if target == "test":
    target_dir = "./input_data/test.csv"
    path = dir + file_name + 'test.csv'

response = requests.get(target)
soup = BeautifulSoup(response.text, 'html.parser')

items = soup.select(
    '#post-7894 > section > div.content > table >tbody > tr')


for item in items:
    item = item.text
    target_text = '公式サイト'

    if target_text in item:
        print(item)


# with open(path, 'w') as f:
#     f.write('name' + ',' + 'link' + ',' + 'genre' + ',' +
#             'limit' + ',' + 'apply' + ',' + 'contract' + '\n')
