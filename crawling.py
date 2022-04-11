# 네이버 뉴스 기사 크롤링 #참고 : https://chan123.tistory.com/67
import pandas as pd
from pandas import Series
import requests
from bs4 import BeautifulSoup

#request: 웹사이트에 요청할 수 있는 기능들을 모아둔 클래스

url_par = requests.get('https://health.chosun.com/news/dailynews_view.jsp?mn_idx=431329')
# request.get() : get() 함수는 웹페이지의 내용을 요청하는 함수, 매개 변수로 웹페이지의 주소를 입력
raw = BeautifulSoup(url_par.text)
# .text 변수를 사용하여 요청 결과를 단순 텍스트로 보여줌

#뉴스 제목 가져오기
news_title = raw.select_one('h2#title_text')
news_title = news_title.get_text()

#뉴스 날짜 가져오기
news_date = raw.select_one('p#date_text')
news_date = news_date.get_text()
news_date = news_date.replace('입력 : ','')
print(news_date)

#뉴스 본문 가져오기 (In Website contents HTML : div# id="news_body_id" class="article fontset_mal" content: p)
news_content = ''
for p in raw.select('div#news_body_id p'):
    news_content +=p.get_text()

#문자열(str)을 열로 만들어서 데이터 프레임 생성하기 (str들을 list에 저장 후 -> dataframe)
title = []
title.append(news_title)
date = []
date.append(news_date)
content = []
content.append(content)
news_table = pd.DataFrame({"date":date,"title":title,"content":content})



'''지정 기간 동안의 기사 크롤링 진행'''

#7월달 뉴스 기사는 426948부터 430954까지 총 4007개이지만, 중간에 비어있는 웹페이지 빼면 "3961개"
num = 0
date = []
title = []
content = []

#원하는 기간 yyyy.mm 형태로 기입
duration = input('수집 기간: (yyyy.mm.dd 형태로 기입)')

for num in range(430954,440000): #1000000(큰수)로 해놓고 해당 기간의 뉴스만 찾아랏!
    url = requests.get('https://health.chosun.com/news/dailynews_view.jsp?mn_idx=' + str(num))
    html = BeautifulSoup(url.text, "html.parser")
    news_date = html.select_one('p#date_text')

    # num 숫자 사이에 빈 페이지가 있다면(없는 페이지가 있다면), continue 뒷문장은 실행 X
    if news_date is None:  # null 값인지 확인할 때 "is None" 사용
        continue
    news_date = news_date.get_text()
    news_date = news_date.replace('입력 : ', '')
    news_date = str(news_date)

#원하는 날짜 기입!
    if duration not in news_date: #news_date에 2021.07이라는 문자가 없다면, continue 뒷문장은 실행 X
        continue

    news_title = html.select_one('h2#title_text')
    news_title = news_title.get_text()
    news_content = ''
    for p in html.select('div#news_body_id p'):
        news_content +=p.get_text()

    title.append(news_title)
    date.append(news_date)
    content.append(news_content)
    print(num)

#여러개의 리스트를 dataframe으로 만들어줌
date = pd.to_datetime(date, format="%Y/%m/%d")
news_table = pd.DataFrame({"date":date,"title":title,"content":content})

#csv파일로 변환!
#이렇게 저장하면 한글깨짐!!
#news_table.to_csv('C:/Users/pouoq/Desktop/TEXT/헬스케어 TM/rawdata_7월.csv')
#이렇게 저장하셈!!
news_table.to_csv('C:/Users/pouoq/Desktop/TEXT/헬스케어 TM/rawdata_8월.csv',encoding='utf-8-sig')
