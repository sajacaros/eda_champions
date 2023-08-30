import configparser
import csv
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def get_chrome_driver(parent_path='..'):
    config = configparser.ConfigParser()
    config.read(f'{parent_path}/config.ini')
    return config['DEFAULT']['path']


# 크롬 드라이버 로드
# pip install selenium --upgrade
# selenium version : 4.11.2
# 익숙하신 selenium 띄우는 코드로 바꾸셔도 무방합니다.
def chrome_driver(path):
    return webdriver.Chrome(service=Service(executable_path=r"{}".format(path)))


# page load
def load_page(driver, year):
    url = r'https://www.capology.com/uk/premier-league/salaries/{}-{}/'
    driver.get(url.format(year, year+1))
    driver.implicitly_wait(30)  # load


# 세팅 버튼 클릭
def popup_setting(driver):
    driver.execute_script(
        "arguments[0].click();",
        driver.find_element(By.XPATH, '//*[@id="league-players"]/div[1]/button/i')
    )
    return driver.find_element(by=By.XPATH, value='//*[@id="league-players"]/div[2]')


# apply 버튼 클릭
def apply_option(driver, popup_web):
    driver.execute_script(
        "arguments[0].click();",
        popup_web.find_element(By.CSS_SELECTOR, '.table-popup-footer > a.button-apply')
    )


# option 세팅
def set_all(driver):
    driver.execute_script(
        "arguments[0].click();",
        driver.find_element(By.LINK_TEXT, 'All')
    )


def crawling_page(driver, csv_writer):
    players_web = driver.find_elements(By.CSS_SELECTOR, 'table.table > tbody > tr')
    for n, player_web in enumerate(players_web):
        stats_web = player_web.find_elements(By.CSS_SELECTOR, 'td')
        # 'name', 'money-w', 'money-y', 'money-a',
        stats = [
            stats_web[0].find_element(By.CSS_SELECTOR, 'a').text,
            re.sub(r'[^0-9]', '', stats_web[1].text),
            re.sub(r'[^0-9]', '', stats_web[2].text),
            re.sub(r'[^0-9]', '', stats_web[3].text)
        ]
        if n%50 == 0:
            print(f'{n}번재 진행중입니다. {stats}')
        csv_writer.writerow(stats)


def start_crawling(driver, year, parent_path='..'):
    # page load
    load_page(driver, year)
    time.sleep(5)
    # click all
    set_all(driver)
    time.sleep(10)

    with open(f'{parent_path}/data/origin/capology/capology_{year}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        feature_names = [
            'name', 'money-w', 'money-y', 'money-a',
        ]
        csv_writer.writerow(feature_names)
        # page
        crawling_page(driver, csv_writer)


def crawling_all_year(driver, parent_path='..'):
    start_year, end_year = 2014, 2022
    for year in range(start_year,end_year+1):
        print(f'{year}년 크롤링 시작')
        start_crawling(driver, year, parent_path)
        print(f'{year}년 크롤링을 완료했습니다')


def crawling_capology(parent_path='..'):
    # 설정값 읽기
    path = get_chrome_driver(parent_path)
    # driver load
    driver = chrome_driver(path)
    crawling_all_year(driver, parent_path)


if __name__ == '__main__':
    crawling_capology()