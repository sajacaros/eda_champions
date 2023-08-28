import configparser
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


url = 'https://1xbet.whoscored.com/Regions/252/Tournaments/2/Seasons/9075/Stages/20934/PlayerStatistics/England-Premier-League-2022-2023'
# url = ‘https://1xbet.whoscored.com/StatisticsFeed/1/GetPlayerStatistics?category=summary&subcategory=offensive&statsAccumulationType=0&isCurrent=true&playerId=&teamIds=&matchId=&stageId=20934&tournamentOptions=2&sortBy=Rating&sortAscending=&age=&ageComparisonType=&appearances=&appearancesComparisonType=&field=Overall&nationality=&positionOptions=&timeOfTheGameEnd=&timeOfTheGameStart=&isMinApp=false&page=1&includeZeroValues=&numberOfPlayersToPick=10’
# 셀리니움 통한 html 추출
# 옵션을 통해 크롬창을 띄우지 않고 백그라운드에서 크롤링 가능
config = configparser.ConfigParser()
config.read('../config.ini')
path = config['DEFAULT']['path']
driver = webdriver.Chrome(service=Service(executable_path=r"{}".format(path)))
# 크롬 브라우저를 통해, 주소로 접근
driver.get(url)
# 팝업 창 대기를 위한 sleep
time.sleep(3)
pop_up_del_button = driver.find_element(By.CSS_SELECTOR, 'body > div.webpush-swal2-container.webpush-swal2-center.webpush-swal2-fade.webpush-swal2-shown > div > div.webpush-swal2-header > button')
pop_up_del_button.click()
# 공격 지표, 모든 플레이어 표시
offensive_button = driver.find_element(By.CSS_SELECTOR, '#stage-top-player-stats-options > li:nth-child(3) > a')
offensive_button.click()
time.sleep(3)
# all_players = driver.find_element(By.XPATH, '//*[@id="apps"]/dd[3]/a')
all_players = driver.find_element(By.LINK_TEXT, 'All players')
all_players.click()

time.sleep(100)