# coding: UTF-8
from optparse import TitledHelpFormatter
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from datetime import datetime
import csv
import random
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    print("コエテコにあるすべてのスクールを収集します")

    # URL
    target = "https://coeteco.jp/campus/brand/list"
    base_url = "https://coeteco.jp/"

    # Web Driver起動
    driver = webdriver.Chrome('./static/chromedriver')
    driver.get(target)

    # ファイル名の指定
    dt = datetime.now()
    dt_str = dt.strftime('%y%m%d%H%M%S')
    dir = './data/'
    file_name = "coeteco-"
    path = dir + file_name + dt_str + '.csv'

    # 初期値設定
    count = 0

    try:
        while True:
            # 暗黙的な待機
            driver.implicitly_wait(30)

            # スクール要素取得
            anchors = driver.find_elements_by_css_selector(
                'body > section > div.c-adu-section__l-body.u-mb-40 > ul > li > div.adu-school-media > div > a')

            # 要素数表示
            count += len(anchors)
            print(count)

            # CSVファイルの出力
            output(path, anchors, base_url)

            # 次のurlを取得
            next = driver.find_element_by_css_selector(
                'body > section > div.pagination-container > nav > span.page.pager-btn.next > a')

            if not next:
                break

            next_url = next.get_attribute("href")

            dynamic_url = urljoin(base_url, next_url)
            print('次のurl')
            print(dynamic_url)

            # 次のページを取得
            driver.get(dynamic_url)

        # Web Driverを停止
        driver.close()

    except:
        print('AccessError')
        print('次のurl:' + dynamic_url)

        # Web Driverを停止
        driver.close()


def output(path, anchors, base_url):
    with open(path, 'a') as f:
        for anchor in anchors:

            # スクール名の取得
            name = anchor.text

            # 案件のurl取得
            url = anchor.get_attribute("href")
            url = urljoin(base_url, url)

            f.write(name + ',' + url + '\n')


if __name__ == "__main__":
    main()
