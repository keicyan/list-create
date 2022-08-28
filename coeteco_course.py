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
    file_name = "coeteco-course-"
    path = dir + file_name + dt_str + '.csv'

    # Web Driver起動
    driver = webdriver.Chrome('./static/chromedriver')

    for row in reader:
        for data in row:
            print(data)
            course_url = data + '/courses'

            # 暗黙的な待機
            driver.get(course_url)
            driver.implicitly_wait(30)
            time.sleep(random.randint(20, 30))

            # スクール名の取得
            try:
                name_elem = driver.find_element_by_css_selector(
                    'body > div.c-result-header > div.c-result-header__content.section-w1050 > div > div.c-school-header__content > div.c-school-header__detail.js-antiscraper > div.c-school-header__ttl > h1')
                name = name_elem.text
            except:
                print('名前が取得できません')
                continue

            # コース数の取得
            try:
                num_elem = driver.find_element_by_css_selector(
                    'body > div.c-result-wrapper.color-bg > section:nth-child(1) > section > h2')
                num = num_elem.text
                num = num.replace('コース・料金(', '')
                num = num.replace('件)', '')

            except:
                print('コース数が取得できません')
                continue

            with open(path, 'a') as f:
                f.write(name + ',' + num + '\n')

            # コース詳細
            try:
                courses_elem = driver.find_elements_by_css_selector(
                    'body > div.c-result-wrapper.color-bg > section:nth-child(1) > section > div > ul > li')
            except:
                print('コースが取得できません')

            for course_elem in courses_elem:

                # urlの取得
                try:
                    url_elem = course_elem.find_element_by_tag_name('a')
                    url = url_elem.get_attribute("href")
                except:
                    print('コースのurlが取得できません')

                # コース名の取得
                try:
                    name_elem = course_elem.find_element_by_class_name(
                        'c-adu-course-mini__ttl')
                    name = name_elem.text
                    name = name.replace(',', '')
                except:
                    print('コース名が取得できません')

                # 説明文
                try:
                    desc_elem = course_elem.find_element_by_class_name(
                        'c-adu-course-mini__desc')
                    desc = desc_elem.text
                    desc = desc.replace(',', '')
                except:
                    print('コースの説明文が取得できません')

                # 金額
                try:
                    cost_elem = course_elem.find_element_by_class_name(
                        'c-adu-course-mini__cost')
                    cost = cost_elem.text
                    cost = cost.replace(',', '')

                except:
                    print('コースの金額が取得できません')

                # 期間
                try:
                    period_elem = course_elem.find_element_by_class_name(
                        'c-adu-course-mini__period')
                    period = period_elem.text
                    period = period.replace(',', '')
                    period = period.replace('\n', '')

                except:
                    print('コースの期間が取得できません')

                with open(path, 'a') as f:
                    f.write(name + ',' + url + ',' + cost +
                            ',' + period + ',' + desc + '\n')

    # Web Driverを停止
    driver.close()


if __name__ == "__main__":
    main()
