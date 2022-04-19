# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random

print("dodaのurlを入力してください")

target = input(">")

print('')

print("取得数の入力（数字）")

num = int(input(">"))

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "doda-"
path = dir + file_name + datetime + '.csv'

if target == "test":
    target = "https://doda.jp/DodaFront/View/JobSearchList.action?k=Laravel&kwc=1&oc=03L&ss=1&preBtn=3&pic=1&ds=0&tp=1&bf=1&mpsc_sid=10&oldestDayWdtno=0&leftPanelType=1&usrclk_searchList=PC-logoutJobSearchList_searchConditionArea_searchButton-ocL-kwdInclude"

    path = dir + file_name + 'test.csv'

response = requests.get(target)

company = []

try:
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(random.randint(1, 10))
        new_company = soup.find_all('span', class_='company')

        company += new_company
        company = list(set(company))
        count = len(company)

        print(count)

        next = soup.select('#jobAll > div > div.boxRight.clrFix > ul.btnTypeSelect02.parts.clrFix > li.btn_r.last > a')
        next_url = next[0].attrs['href']
        print(next_url)

        if count >= num:
            break

        response = requests.get(next_url)

    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + '\n')
        for item in company:
            f.write(item.get_text() + ',' + '\n')
        f.write(next_url)

except:
    print('AccessError')
    print('次のurl:' + next_url)
    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + '\n')
        for item in company:
            f.write(item.get_text() + ',' + '\n')
        f.write(next_url)
