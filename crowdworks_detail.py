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
print("データファイルのパスを入力してください")

target = input(">")
target_dir = './input_data/' + target + '.csv'

print('')

print("取得数の入力（数字）")

num = int(input(">"))

# ファイル名の指定
dt_now = datetime.datetime.now()
datetime = dt_now.strftime('%y%m%d%H%M%S')
dir = './data/'
file_name = "crowdworks-details-"
path = dir + file_name + datetime + '.csv'

if target == "test":
    target_dir = "./input_data/test.csv"
    path = dir + file_name + 'test.csv'

f = open(target_dir, 'r')
reader = csv.reader(f)

count = 0

with open(path, 'w') as f:
    f.write('name' + ',' + 'link' + ',' + 'genre' + ',' +
            'limit' + ',' + 'apply' + ',' + 'contract' + '\n')

    for row in reader:
        for data in row:
            print(data)
            response = requests.get(data)
            soup = BeautifulSoup(response.text, 'html.parser')
            # time.sleep(random.randint(1, 5))

            error_index = soup.find(class_='error-index')

            if error_index:
                print('ログインが必要なページです')
                continue

            error_page = soup.find(class_='error')

            if error_page:
                print('ページが見つかりません')
                continue

            link = data

            title = soup.select_one(
                '#job_offer_detail > div.cw-row.has_sticky.job_detail > div.cw-column.main > section.cw-section.job_offer_detail_header.no-margin-top > div.title_container.title_detail > h1')
            span = title.select_one('span')

            if not span.is_empty_element:
                title.span.extract()

            genre = soup.select_one(
                '#job_offer_detail > div > div.cw-column.main > section.cw-section.toplevel_information > table > tbody > tr:nth-child(1) > th > div')

            limit = soup.select_one(
                '#job_offer_detail > div.cw-row.has_sticky.job_detail > div.cw-column.main > section.cw-section.toplevel_information > table > tbody > tr:nth-child(4) > td'
            )

            tb = soup.select_one(
                '#job_offer_detail > div.cw-row.has_sticky.job_detail > div.cw-column.main > section.cw-section.application_status > table')

            tb = tb.select('tr td')
            tb_num = len(tb)

            if not tb_num == 4:
                print('データがありません')
                continue

            # 応募人数
            apply = tb[0]

            # 契約した人
            contract = tb[1]

            # 募集人数
            # contract = tb[2]

            # 案件名の取得
            title_text = title.text
            title_text = title_text.strip()
            title_text = title_text.replace(' ', '')
            title_text = title_text.replace(',', '')

            # 就業タイプの取得
            genre_text = genre.text
            genre_text = genre_text.strip()
            genre_text = genre_text.replace(' ', '')
            genre_text = genre_text.replace(',', '')

            # 募集期限の取得
            limit_text = limit.text
            limit_text = limit_text.strip()
            limit_text = limit_text.replace(' ', '')
            limit_text = limit_text.replace(',', '')

            # 募集期限の取得
            apply_text = apply.text
            apply_text = apply_text.strip()
            apply_text = apply_text.replace(' ', '')
            apply_text = apply_text.replace(',', '')
            apply_text = apply_text.replace('人', '')

            # 募集期限の取得
            contract_text = contract.text
            contract_text = contract_text.strip()
            contract_text = contract_text.replace(' ', '')
            contract_text = contract_text.replace(',', '')
            contract_text = contract_text.replace('人', '')

            f.write(title_text + ',' + link + ',' + genre_text + ',' +
                    limit_text + ',' + apply_text + ',' + contract_text + ',' + '\n')

            count += 1
            print(count)

            if count >= num:
                break

        if count >= num:
            break
