# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random


def main():

    print("Angel Portのurlを入力してください")

    target = input(">")

    print('')

    print("取得数の入力（数字）")

    num = int(input(">"))

    # ファイル名の指定
    dt = datetime.datetime.now()
    dt_now = dt.strftime('%y%m%d%H%M%S')
    dir = './data/'
    file_name = "angel-"
    path = dir + file_name + dt_now + '.csv'

    if target == "test":
        target = "https://angl.jp/companies"

        path = dir + file_name + 'test.csv'

    response = requests.get(target)

    base_url = "https://angl.jp/"
    company = []

    try:
        while True:
            soup = BeautifulSoup(response.text, 'html.parser')
            # time.sleep(random.randint(1, 10))

            new_company = soup.select('#investments > div > div > a')

            company += new_company
            company = list(set(company))
            count = len(company)

            print(count)

            next = soup.select_one(
                'body > div.container > div > div.col-11.col-lg-10.text-center.mb-4 > nav > span.next > a')
            next_url = next.attrs['href']

            if count >= num:
                break

            print(next_url)
            dynamic_url = urljoin(base_url, next_url)
            response = requests.get(dynamic_url)

        # CSVファイルの出力
        output(path, company, dynamic_url, base_url)

    except:
        print('AccessError')
        print('次のurl:' + dynamic_url)
        # CSVファイルの出力
        output(path, company, dynamic_url, base_url)


def output(path, company, dynamic_url, base_url):
    with open(path, 'w') as f:
        f.write('name' + ',' + 'url' + '\n')
        for item in company:
            # url
            url = item.attrs['href']
            url = urljoin(base_url, url)

            # 会社名
            name = item.text
            name = name.strip()
            name = name.replace(',', '')
            name = name.replace('\n', '')

            f.write(name + ',' + url + '\n')

        f.write(dynamic_url)


if __name__ == "__main__":
    main()
