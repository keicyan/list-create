# coding: UTF-8
from optparse import TitledHelpFormatter
from urllib.parse import urljoin
from datetime import datetime
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():

    print("案件情報収集用")
    print("クラウドワークスのurlを入力してください")

    target = input(">")

    # ファイル名の指定
    dt = datetime.now()
    dt_str = dt.strftime('%y%m%d%H%M%S')
    dir = './data/'
    file_name = "crowdworks-"
    path = dir + file_name + dt_str + '.csv'

    if target == "test":
        target = "https://crowdworks.jp/public/jobs/category/14"
        path = dir + file_name + 'test.csv'

    with open(path, 'w') as f:
        f.write(target + '\n' + 'name' + ',' + 'link' + ',' +
                        'job' + ',' + 'fee' + '\n')

    # Web Driver起動
    driver = webdriver.Chrome('./static/chromedriver')
    driver.implicitly_wait(60)

    # ページの表示
    driver.get(target)

    count = []

    try:
        while True:
            driver.implicitly_wait(random.randint(5, 30))

            titles = driver.find_elements_by_css_selector(
                '#result_jobs > div.search_results > ul > li > div > div > div.item_body.job_data_body > div.job_data_row > div.job_data_column.summary > h3 > a')

            jobs = driver.find_elements_by_css_selector(
                '#result_jobs > div.search_results > ul > li > div > div > div.item_body.job_data_body > div.job_data_row > div.job_data_column.entry > div > div.entry_data.payment > div > span'
            )

            fees = driver.find_elements_by_css_selector(
                '#result_jobs > div.search_results > ul > li > div > div > div.item_body.job_data_body > div.job_data_row > div.job_data_column.entry > div > div.entry_data.payment > div > b'
            )

            count += titles
            print(len(count))

            next = driver.find_elements_by_css_selector(
                '#result_jobs > div.search_sub_menus.bottom > a')

            if not next:
                break

            next_url = next[0].get_attribute('href')

            # CSVファイルの出力
            write_csv(path, titles, jobs, fees)

            driver.get(next_url)

    except:
        print('AccessError')
        print('次のurl:' + next_url)

        with open(path, 'a') as f:
            f.write(next_url)

def write_csv(path, titles, jobs, fees):
    with open(path, 'a') as f:

        for (title, job, fee) in zip(titles, jobs, fees):

            # 案件名の取得
            title_text = title.text
            title_text = title_text.replace(' ', '')
            title_text = title_text.replace(',', '')

            # 案件のurl取得
            url = title.get_attribute('href')

            # 勤務形態の取得
            job_text = job.text

            # 給与の取得
            fee = fee.text
            fee = fee.strip()
            fee = fee.replace(' ', '')
            fee_text = fee.replace(',', '')

            f.write(title_text + ',' + url + ',' +
                    job_text + ',' + fee_text + ',' + '\n')

if __name__ == "__main__":
    main()