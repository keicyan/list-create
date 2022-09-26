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
    print("比較bizにあるすべての企業を収集します")

    # URL
    target = "https://www.biz.ne.jp/list/web-system/"
    base_url = "https://www.biz.ne.jp/"

    # Web Driver起動
    driver = webdriver.Chrome('./static/chromedriver')
    driver.get(target)

    # ファイル名の指定
    dt = datetime.now()
    dt_str = dt.strftime('%y%m%d%H%M%S')
    dir = './data/'
    file_name = "biz-"
    path = dir + file_name + dt_str + '.csv'

    # 初期値設定
    count = 0

    try:
        while True:
            # 暗黙的な待機
            driver.implicitly_wait(30)

            # 会社名要素取得
            titles = driver.find_elements_by_css_selector(
                '#list > ul > li > div > h3')

            print('ここにはきてる？')

            anchors = driver.find_elements_by_class_name(
                '#list > ul > li> div > div.result_outline.flex_in > div.right > div > a')

            # 要素数表示
            count += len(titles)
            print(count)

            # CSVファイルの出力
            output(path, titles, anchors, base_url)

            # 次のurlを取得
            next = driver.find_elements_by_css_selector(
                '#list > div.center > div > ul > li.beforenext > a')
            next = next[-2]

            if count > 900:
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


def output(path, titles, anchors, base_url):
    with open(path, 'a') as f:
        for title, anchor in zip(titles, anchors):

            # スクール名の取得
            name = title.text

            # 案件のurl取得
            url = anchor.get_attribute("href")
            url = urljoin(base_url, url)

            f.write(name + ',' + url + '\n')


if __name__ == "__main__":
    main()
