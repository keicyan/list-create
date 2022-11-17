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

    print("typeの詳細データを取得します")

    print("type のurlを入力してください")

    target = input(">")

    if target == "test":
        target = "https://type.jp/job/search.do?pathway=4&job3IdList=3&job3IdList=129&job3IdList=13&job3IdList=130&job3IdList=4&job3IdList=9&job3IdList=6&job3IdList=10&job3IdList=15&job3IdList=18&job3IdList=5&job3IdList=14&job3IdList=131&job3IdList=20&job3IdList=21&job3IdList=29&job3IdList=22&job3IdList=45&job3IdList=47&job3IdList=27&job3IdList=28&job3IdList=30&job3IdList=31&job3IdList=32&job3IdList=132&job3IdList=133&job3IdList=33&salaryId="

    base_url = "https://type.jp/"

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
                    '#content > div > div > main > form > section.job-list.right-column > div.js-cloned-mod-pagination > article > div > header > h2 > p > span')

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
                '#content > div > div > main > form > section.job-list.right-column > div.mod-pagination.mb0.mt30 > p.next.active > a')
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
    file_name = "type-"
    path = dir + file_name + dt_str + '.csv'

    with open(path, 'w') as f:
        f.write('title' + ',' + '\n')

        for elem in list:
            f.write(elem + ',' + '\n')

        f.write(dynamic_url)


if __name__ == "__main__":
    main()
