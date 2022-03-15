import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv

print("indeedのurlを入力してください")

target = input(">")

response = requests.get(target)

print('')

print("取得数の入力（数字）")

num = int(input(">"))

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
path = dir + datetime + '.csv'

base_url = "https://jp.indeed.com/"
company = []

try:
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')
        new_company = soup.find_all('span', class_='companyName')

        company += new_company
        company = list(set(company))
        count = len(company)

        print(count)

        next = soup.find('a', attrs={'aria-label':'次へ'})
        print(next.get("href"))

        if count >= num:
            break

        # 次のページのurlの取得
        dynamic_url = urljoin(base_url, next.get("href"))
        response = requests.get(dynamic_url)

    # 会社名の出力
    for item in company:
        print(item.get_text())

    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + '\n')
        for item in company:
            f.write(item.get_text() + ',' + '\n')

except:
    print('AccessError')

    # 会社名の出力
    for item in company:
        print(item.get_text())

    # CSVファイルの出力
    with open(path, 'w') as f:
        for item in company:
            f.write(item.get_text() + ',' + '\n')
