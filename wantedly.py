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

    print("wantedlyの詳細データを取得します")

    print("wontedly のurlを入力してください")

    target = input(">")

    if target == "test":
        target = "https://www.wantedly.com/projects?type=mixed&page=1&occupation_types%5B%5D=jp__engineering&occupation_types%5B%5D=jp__pm_and_web_direction&locations%5B%5D=sapporo"

    base_url = "https://www.wantedly.com/"

    # 初期値
    company_list = []
    same_count = 0
    base_count = 0

    # Web Driver起動
    driver = webdriver.Chrome('./static/chromedriver')
    driver.implicitly_wait(60)

    # ページの表示
    driver.get(target)

    try:
        while True:
            # ページ内全件取得
            try:
                company_elems = driver.find_elements_by_css_selector(
                    '#project-index > div.two-column.left-side-bar.cf > div.column-main > div > div.projects-index-list > article > div > div.project-bottom > div.company-name > h3 > a')

                # 取得数の表示
                get_count = len(company_elems)
                print('取得数', end=':')
                print(get_count)
            except:
                print('リストが取得できません')

            for company_elem in company_elems:
                # 会社名の取得
                try:
                    name = company_elem.text
                    name = name.replace(',', '')

                    company_list.append(name)

                except:
                    print('会社名が取得できません')

            company_list = list(set(company_list))
            count = len(company_list)
            print('合計', end=':')
            print(count)

            # 次のページのurlを取得
            url_elem = driver.find_element_by_css_selector(
                '#project-index > div.two-column.left-side-bar.cf > div.column-main > div > div.project-index-pagination > nav > span.next > a')
            next_url = url_elem.get_attribute("href")
            print(next_url)

            dynamic_url = urljoin(base_url, next_url)

            if count == base_count:
                same_count += 1

            if same_count == 10:
                break

            driver.implicitly_wait(60)
            driver.get(dynamic_url)

            base_count = count

        # CSVファイルの出力
        output(company_list, dynamic_url)

        # Web Driverを停止
        driver.close()

    except:
        print('AccessError')
        print('次のurl:' + dynamic_url)
        # CSVファイルの出力
        output(company_list, dynamic_url)

        # Web Driverを停止
        driver.close()


def output(list, dynamic_url):
    # メインファイル名の指定
    dt = datetime.now()
    dt_str = dt.strftime('%y%m%d%H%M%S')
    dir = './data/'
    file_name = "wantedly-"
    path = dir + file_name + dt_str + '.csv'

    with open(path, 'w') as f:
        f.write('title' + ',' + '\n')

        for elem in list:
            f.write(elem + ',' + '\n')

        f.write(dynamic_url)


if __name__ == "__main__":
    main()
