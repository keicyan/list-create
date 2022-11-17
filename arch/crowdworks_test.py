# coding: UTF-8
from optparse import TitledHelpFormatter
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import datetime
import csv
import random

print("案件情報収集用")
print("クラウドワークスのurlを入力してください")

target = input(">")

print('')

print("取得数の入力（数字）")

num = int(input(">"))

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "crowdworks-"
path = dir + file_name + datetime + '.csv'

if target == "test":
    target = "https://crowdworks.jp/public/jobs/category/241"

    path = dir + file_name + 'test.csv'

response = requests.get(target)

base_url = "https://crowdworks.jp/"

titles = []
jobs = []
fees = []

try:
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(random.randint(1, 10))

        new_title = soup.select(
            '#result_jobs > div.search_results > ul > li > div > div > div.item_body.job_data_body > div.job_data_row > div.job_data_column.summary > h3 > a')

        new_job = soup.select(
            '#result_jobs > div.search_results > ul > li > div > div > div.item_body.job_data_body > div.job_data_row > div.job_data_column.entry > div > div.entry_data.payment > div > span'
        )

        new_fee = soup.select(
            '#result_jobs > div.search_results > ul > li > div > div > div.item_body.job_data_body > div.job_data_row > div.job_data_column.entry > div > div.entry_data.payment > div > b'
        )

        titles += new_title
        jobs += new_job
        fees += new_fee

        count = len(titles)
        print(count)

        next = soup.select(
            '#result_jobs > div.search_sub_menus.upper > div.cw-pull_right > div > div > a.next_page')

        if not next:
            break

        next_url = next[0].attrs['href']

        dynamic_url = urljoin(base_url, next_url)
        print(dynamic_url)
        response = requests.get(dynamic_url)

        if count >= num:
            break

    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + 'link' + ',' +
                'job' + ',' + 'fee' + '\n')

        for (title, job, fee) in zip(titles, jobs, fees):

            # 案件名の取得
            title_text = title.text
            title_text = title_text.replace(' ', '')
            title_text = title_text.replace(',', '')

            # 案件のurl取得
            url = title.get('href')
            url = urljoin(base_url, url)

            # 勤務形態の取得
            job_text = job.text

            # 給与の取得
            fee = fee.get_text()
            fee = fee.strip()
            fee = fee.replace(' ', '')
            fee_text = fee.replace(',', '')

            f.write(title_text + ',' + url + ',' +
                    job_text + ',' + fee_text + ',' + '\n')

        f.write(dynamic_url)

except:
    print('AccessError')
    print('次のurl:' + dynamic_url)
    # CSVファイルの出力
    with open(path, 'w') as f:
        f.write('name' + ',' + 'link' + ',' +
                'job' + ',' + 'fee' + '\n')

        for (title, job, fee) in zip(titles, jobs, fees):

            # 案件名の取得
            title = title.find('a')
            title = title.text
            title = title.replace(' ', '')
            title_text = title.replace(',', '')

            # 案件のurl取得
            list_url = title.get('href')

            # 勤務形態の取得
            job_text = job.text

            # 給与の取得
            fee = fee.get_text()
            fee = fee.strip()
            fee = fee.replace(' ', '')
            fee_text = fee.replace(',', '')

            f.write(title_text + ',' + list_url + ',' +
                    job_text + ',' + fee_text + ',' + '\n')

        f.write(dynamic_url)
