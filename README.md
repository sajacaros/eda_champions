# eda_champions
## 목표
* 특정 선수의 스텟 확인 및 평균과의 비교
## crawling
* 1xbet
  * player's stats
* understat
  * player's stats
* capology
  * player's salary
* spotrac
  * player's salary
## feature engineering
* player
  * 크롤링한 데이터로부터 player 데이터 생성
* 나이 레벨링
  * 나이를 레벨링 데이터로 변환
  * order를 주기위해 타입을 Category로 변경
``` 
age_order = ['<21', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '32<']
```
## 결측 데이터
* player와 데이터 결합시 결측률 30%를 넘음
  * 이름의 변환
    * 영어 이름이 아닌 경우 영어로 변환
    * 성과 이름의 어순이 바뀐 경우 통일되도록 수정
    * 불필요한 이름 데이터 처리(ex> 괄호)
  * 추가적인 연봉 데이터 수집(capology 크롤링 추가)
* 위의 작업을 통해 데이터 결합시 결측률 3%를 기록함
  * 나머지 데이터는 버림
## 데이터 분석
* 포지션별 중요 스텟 파악
``` 
'General': ['ADJ Salary', 'Apps', 'Min'],
'Forward-o': ['G', 'xG', 'NPG', 'A', 'xA', 'Drb_Off'],
'Forward-d': ['Tackles', 'Inter'],
'Midfielder-o': ['G', 'xG', 'A', 'xA', 'xGBuildup', 'KeyP', 'Drb_Off', 'AvgP', 'PS%'],
'Midfielder-d': ['Tackles', 'Inter', 'Clear', 'Blocks'],
'Defender-o': ['G', 'xG', 'A', 'xA', 'xGBuildup', 'AvgP', 'PS%'],
'Defender-d': ['Tackles', 'Inter', 'Clear', 'Blocks', 'Drb_Def'],
'Goalkeeper-o': ['xGBuildup', 'AvgP', 'PS%'],
'Goalkeeper-d': ['Tackles', 'Inter', 'Clear', 'Blocks', 'Drb_Def']
```
* 선수의 스텟간 분포 분석
* 나이 레벨에 따른 같은 포지션의 선수들 평균과 비교
* 선수의 년도에 따른 포지션 변화 분석
* 선수와 비슷한 스타일 분석
## 시각화
* 웹을 통해 선수 검색 및 분석 결과 제공
## 기타
* 용어 사전 제공
## 설치
```
pip install dash
pip install dash-bootstrap-components
pip install numpy
pip install pandas
pip install seaborn
pip install scikit-learn
```
## 실행
``` 
python eda_project.py
```
## 참고 문서
* plotly
  * [line charts](https://plotly.com/python/line-charts/) 
  * [histogram](https://plotly.com/python/histograms/)
  * [distplot](https://plotly.com/python/distplot/)
  * [box plot](https://plotly.com/python/box-plots/)
* [dash-bootstrap-components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/)
* [Plotly Tutorial - wikidocs](https://wikidocs.net/book/8909)
* [pep-0008](https://peps.python.org/pep-0008/#import)
