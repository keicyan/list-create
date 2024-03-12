# coding: UTF-8
from optparse import TitledHelpFormatter
from urllib.parse import urljoin
from datetime import datetime
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    # 取得URLの設定
    print("indeedのurlを入力してください")

    target = input(">")

    # 保存先の設定
    dt = datetime.now()
    dt_str = dt.strftime('%y%m%d%H%M%S')
    dir = './data/'
    file_name = "indeed-"
    path = dir + file_name + dt_str + '.csv'

    # テストモードの設定
    if target == "test":
        target = "https://jp.indeed.com/jobs?q=%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2%E3%80%80%E5%8F%97%E8%A8%97&l=&vjk=55d699e40649d5c3&advn=1440220986574916"
        path = dir + file_name + 'test.csv'

    # Web Driver起動
    driver = webdriver.Chrome('./static/chromedriver')
    driver.implicitly_wait(60)

    # ページの表示
    driver.get(target)

    company_list = []

    try:
        while True:
            driver.implicitly_wait(random.randint(5, 30))

            company_elements = driver.find_elements_by_css_selector(
                '#mosaic-provider-jobcards > ul > li > div > div.slider_container.css-12igfu2.eu4oa1w0 > div > div > div > table.css-1v79ar.eu4oa1w0 > tbody > tr > td > div.company_location.css-104iw4m.e37uo190 > div > span')

            for item in company_elements:
                company_name = item.text
                company_list.append(company_name)

            # 取得数の表示
            company_list = list(set(company_list))
            count = len(company_list)

            # 次のページのURLを取得
            next = driver.find_element_by_css_selector('[data-testid="pagination-page-next"]')
            next_url = next.get_attribute('href')
            driver.get(next_url)

            # ログの表示
            print(count)
            print(next_url)

            if not next:
                break

        # CSVファイルの出力
        write_csv(path, company_list, next_url)

        # Web Driverを停止
        driver.close()

    except:
        print('AccessError')
        print('次のurl:' + next_url)
        # CSVファイルの出力
        write_csv(path, company_list, next_url)

        # Web Driverを停止
        driver.close()

def write_csv(path, list, url):
    with open(path, 'w') as f:
        f.write('name' + ',' + '\n')
        for item in list:
            f.write(item + ',' + '\n')
        f.write(url)

if __name__ == "__main__":
    main()