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
    file_name = "coeteco-feature-"
    path = dir + file_name + dt_str + '.csv'

    # Web Driver起動
    driver = webdriver.Chrome('./static/chromedriver')

    for row in reader:
        for data in row:
            print(data)

            # 暗黙的な待機
            driver.implicitly_wait(30)
            time.sleep(random.randint(10, 20))
            driver.get(data)

            # スクール名の取得
            try:
                name_elem = driver.find_element_by_css_selector(
                    'body > div.c-result-header > div.c-result-header__content.section-w1050 > div > div.c-school-header__content > div.c-school-header__detail.js-antiscraper > div.c-school-header__ttl > h1')
                name = name_elem.text
            except:
                print('名前が取得できません')
                continue

            # 特徴
            try:
                obj_elems = driver.find_elements_by_css_selector(
                    'body > section > section > div > div.l-school-sec__aside > table > tbody > tr:nth-child(4) > td > ul > li > img')
                objs = ''
                for obj_elem in obj_elems:
                    obj = obj_elem.get_attribute('alt')
                    objs += ' ' + obj

            except:
                print('特徴が取得できません')
                continue

            with open(path, 'a') as f:
                f.write(name + ',' + objs + '\n')


if __name__ == "__main__":
    main()
