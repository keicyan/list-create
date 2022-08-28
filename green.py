import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random

print("Greenのurlを入力してください")

target = input(">")

if target == "test":
    target = "https://www.green-japan.com/search_key/01?key=5nkvuljolntvgrqdbqne&keyword=Laravel"

response = requests.get(target)

print('')

print("取得数の入力（数字）")

num = int(input(">"))

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "green-"
path = dir + file_name + datetime + '.csv'

base_url = "https://www.green-japan.com"
company = []

try:
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(random.randint(1, 5))
        new_company = soup.find_all(
            'h3', class_='card-info__detail-area__box__title')

        company += new_company
        company = list(set(company))
        count = len(company)

        print(count)

        next = soup.find('a', class_='next_page')
        print(next.get("href"))

        if count >= num:
            break

        # 次のページのurlの取得
        dynamic_url = urljoin(base_url, next.get("href"))
        response = requests.get(dynamic_url)

    print('次のurl:' + dynamic_url)

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
