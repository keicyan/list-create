# coding: UTF-8
from optparse import TitledHelpFormatter
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from datetime import datetime
import csv
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    print("コエテコの詳細データを取得します")

    target = 'coeteco'
    target_dir = './input_data/' + target + '.csv'

    f = open(target_dir, 'r')
    reader = csv.reader(f)

    # メインファイル名の指定
    dt = datetime.now()
    dt_str = dt.strftime('%y%m%d%H%M%S')
    dir = './data/'
    file_name = "coeteco-details-"
    path = dir + file_name + dt_str + '.csv'

    # Web Driver起動
    driver = webdriver.Chrome('./static/chromedriver')

    for row in reader:
        for data in row:
            print(data)

            # 暗黙的な待機
            driver.implicitly_wait(30)
            time.sleep(random.randint(20, 30))
            driver.get(data)

            # スクール名の取得
            try:
                name_elem = driver.find_element_by_css_selector(
                    'body > div.c-result-header > div.c-result-header__content.section-w1050 > div > div.c-school-header__content > div.c-school-header__detail.js-antiscraper > div.c-school-header__ttl > h1')
                name = name_elem.text
            except:
                print('名前が取得できません')
                continue

            # LPの取得
            try:
                url_elem = driver.find_element_by_css_selector(
                    'body > div.c-result-header > div.c-result-header__content.section-w1050 > div > div.c-school-header__btn-area > div > a')
                url = url_elem.get_attribute("href")
            except:
                print('url is not found')
                url = 'url is not found'

            # 評価の値取得
            try:
                val_elem = driver.find_element_by_css_selector(
                    'body > div.c-result-header > div.c-result-header__content.section-w1050 > div > div.c-school-header__content > div.c-school-header__detail.js-antiscraper > div.c-review-rating > span.c-review-rating__val')
                val = val_elem.text
            except:
                print('口コミの数が足りません')
                continue

            # レビュー数
            try:
                num_elem = driver.find_elements_by_css_selector(
                    'body > div.c-result-header > div:nth-child(2) > nav > div > ul > li > a > p.c-page-nav-campus__badge > span')

                val_num = num_elem[0].text
            except:
                print('口コミの数が足りません')
                continue

            # コース数
            try:
                corse_num = num_elem[1].text
            except:
                print('口コミの数が足りません')
                continue

            # 授業形式
            try:
                lesson_elem = driver.find_element_by_css_selector(
                    'body > section > section > div > div.l-school-sec__aside > table > tbody > tr:nth-child(1) > td')
                lesson = lesson_elem.text
            except:
                print('授業形式が取得できません')
                continue

            # 学習目的
            try:
                obj_elem = driver.find_element_by_css_selector(
                    'body > section > section > div > div.l-school-sec__aside > table > tbody > tr:nth-child(2) > td')
                obj = obj_elem.text
            except:
                print('学習目的が取得できません')
                continue

            with open(path, 'a') as f:
                f.write(name + ',' + url + ',' + val + ',' +
                        val_num + ',' + corse_num + ',' + lesson + ',' + obj + '\n')

    # Web Driverを停止
    driver.close()


if __name__ == "__main__":
    main()
