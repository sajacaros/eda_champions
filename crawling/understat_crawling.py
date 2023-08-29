import configparser
import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup


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
    url = r'https://understat.com/league/EPL/{}'
    driver.get(url.format(year))
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
def set_options(driver, popup_web):
    option_inputs = popup_web.find_elements(by=By.CSS_SELECTOR, value='.row-display > input')
    checked_list = [
        False, True, True, True, True,  # no, Player, Team, Apps, Min
        True, True, True, True, True,  # G, NPG, A, xG, NPxG
        True, True, True, True, True,  # xA, xGChain, xGBuildup, xG90, NPxG90
        True, True, True, True, True  # xA90, xG90+xA90, NPxG90+xA90, xGChain90, xGBuildup90
    ]
    for o_input, o_check in zip(option_inputs, checked_list):
        if o_input.get_property('checked') is not o_check:
            driver.execute_script("arguments[0].click();", o_input)
    apply_option(driver, popup_web)


def attr_to_list(player_attrs):
    return [
        player_attrs[0].select_one('a')['href'][7:],
        player_attrs[0].select_one('a').text,
        player_attrs[1].select_one('a').text,
        player_attrs[2].text,
        player_attrs[3].text,
        player_attrs[4].text,
        player_attrs[5].text,
        player_attrs[6].text,
        player_attrs[7].find(string=True),
        player_attrs[8].find(string=True),
        player_attrs[9].find(string=True),
        player_attrs[10].text,
        player_attrs[11].text,
        player_attrs[12].text,
        player_attrs[13].text,
        player_attrs[14].text,
        player_attrs[15].text,
        player_attrs[16].text,
        player_attrs[17].text,
        player_attrs[18].text,
    ]


def get_stats(players_html):
    players = players_html.select('#league-players>table>tbody')[0].select('tr')
    ret = []
    for player in players:
        player_attrs = player.select('td')
        if player_attrs[0].select_one('a') is None:
            continue
        ret.append(attr_to_list(player_attrs))
    return ret


def travel_page(driver, page_list, n, csv_writer):
    for page in page_list:
        num = page.get_attribute('data-page')
        if num is not None and int(num) == n:
            print(f'{n} page 이동')
            driver.execute_script("arguments[0].click();", page.find_element(By.CSS_SELECTOR, 'a'))
            time.sleep(1)
            stats = get_stats(BeautifulSoup(driver.page_source, 'html.parser'))
            csv_writer.writerows(stats)
            print(f'{n} page 크롤링 완료')
            return


def crawling_page(driver, csv_writer):
    start_page = 1
    last_page = int(driver.find_element(By.CSS_SELECTOR, 'ul.pagination > li:nth-last-child(1) > a').text)
    print(start_page, last_page)
    for n in range(start_page, last_page + 1):
        page_list = driver.find_elements(By.CSS_SELECTOR, 'ul.pagination > li')
        travel_page(driver, page_list, n, csv_writer)
        time.sleep(1)


def start_crawling(driver, year, parent_path='..'):
    # page load
    load_page(driver, year)
    time.sleep(5)
    # popup setting
    popup_web = popup_setting(driver)
    time.sleep(1)
    # setting option
    set_options(driver, popup_web)
    with open(f'{parent_path}/data/understat_{year}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        feature_names = [
            'No', 'Player', 'Team', 'Apps', 'Min',
            'G', 'NPG', 'A', 'xG', 'NPxG',
            'xA', 'xGChain', 'xGBuildup', 'xG90', 'NPxG90',
            'xA90', 'xG90+xA90', 'NPxG90+xA90', 'xGChain90', 'xGBuildup90'
        ]
        csv_writer.writerow(feature_names)
        # page
        crawling_page(driver, csv_writer)


def crawling_all_year(driver, parent_path='..'):
    start_year, end_year = 2014, 2022
    for year in range(start_year,end_year+1):
        print(f'{year}년 크롤링 시작')
        start_crawling(driver, year, parent_path)


def crawling_understat(parent_path='..'):
    # 설정값 읽기
    path = get_chrome_driver(parent_path)
    # driver load
    driver = chrome_driver(path)
    crawling_all_year(driver, parent_path)


if __name__ == '__main__':
    crawling_understat()
