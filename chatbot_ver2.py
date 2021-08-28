#################################################################### chat bot #####################################################################
## In The FOREST                                                                                                                                 ##
## edit 2021.07.13                                                                                                                               ##
##                                                                                                                                               ##
## (News Web Site)                                                                                                                               ##
## 1. The Hacker News (ENG)                                                                                                                      ##
## 2. Boan News (KOR)                                                                                                                            ##
## 3. Daily Secu (KOR)                                                                                                                           ##
## 4. Wired (ENG)                                                                                                                                ##
## 5. Google project zero (ENG)                                                                                                                  ##
##                                                                                                                                               ##
## (Error Web Site)                                                                                                                              ##
## 1. Info Security                                                                                                                              ##
##                                                                                                                                               ##
## (Function)                                                                                                                                    ##
## 1. Today's News                                                                                                                               ##
## 2. Weekly Hot News                                                                                                                            ##
## 3. Search Topic                                                                                                                               ##
## 4. Recommend News                                                                                                                             ##
###################################################################################################################################################
import requests
import datetime
import time
import random
import multiprocessing as mp
import os
import hashlib
# from flask import Flask                                       ### 카카오 i 에서 직접 실험을 통해 import 할지에 대한 판단이 필요
from bs4 import BeautifulSoup
from googletrans import Translator                              ########## googletrans에서 언제라도 막을 수 있음. 대체 방안 찾기 ##########
## ㄴ 구름으로 실행시 오류 발생

from selenium import webdriver                                  ### 검색어 (해시테그?)
from webdriver_manager.chrome import ChromeDriverManager

import socket

# from apscheduler.schedulers.blocking import BlockingScheduler   ### used for update in website

## JUST FOR TEST ##
# application = Flask(__name__)

# @application.route("/")
# def test():
#     return "hello groom!"

# @application.route("/today")
# def today():
#     return "worked"
    # d_today = datetime.datetime.now()
    # dat = d_today.strftime('%B %d, %Y')
    # dat = "July 04, 2021"
    # headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}
    # url = "https://thehackernews.com/"
    # res = requests.get(url, headers=headers)
    # res.raise_for_status()
    # soup = BeautifulSoup(res.text, "lxml")
    # posts = soup.find_all("div", attrs={"class":"body-post clear"})
    # cnt = 0
    # ans = 'The Hacker News'
    # for post in posts:
    #     date_name = post.find("div", attrs={"class":"item-label"}).get_text() # 날짜 + 작성자
    #     if (dat != date_name[1:len(dat)+1]):            # same date (compare with today)
    #         break

    #     title = post.find("h2", attrs={"class":"home-title"}).get_text()            # title of the article
    #     # print(title)

    #     result = translator.translate(title, src='en', dest="ko")           # translate to korean
    #     print(result.text)

    #     link = post.find("a", attrs={"class":"story-link"})["href"]         # article's URL
    #     print(link)

    #     cnt += 1


########### (위) 카카오톡 챗봇을 위해 구현 ################
########### (아래) 웹 스크래핑 틀 ###############

##### Flask, Django -> 카카오 i 신청 접수 성공 시 해보기 (ver2, ver2_2)

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}

# translator = Translator()

#################################################################### show function ####################################################################

def funcText():
    print("-----------기능-----------")
    print("오늘의 보안 뉴스 : 오늘, ㅇㄴ, 오늘의 뉴스\n")
    print("한 주간 HOT 보안 뉴스 : 주간, ㅈㄱ\n")
    print("보안 뉴스 검색 : 검색, ㄱㅅ, ㄳ\n")
    print("구글's 제로프로젝트: 구글제로프로젝트\n")
    print("챗봇 끄기 : 종료, ㅈㄹ\n")

######################################################################################################################################################


#################################################################### SHA1 ####################################################################
# 해시 값으로 바꿈
def sha1_hash(ID):
    text = ID.encode('utf-8')
    sha1 = hashlib.new("sha1")
    sha1.update(text)
    result = sha1.hexdigest()
    return result

######################################################################################################################################################


#################################################################### start ####################################################################

def s():
    print("-------chatbot v0.1-------\n")

    home_path = os.path.expanduser('~')     # home directory
    print(home_path)
    path = home_path + '\\logfile'
    os.makedirs(path, exist_ok=True)

    # print(socket.gethostname()
    unhashed = socket.gethostbyname(socket.gethostname())
    hashed_usr = sha1_hash(unhashed)
    print(hashed_usr)
    # ### USER identification ###
    # path = ''
    # hashed_usr = ''
    # while 1:
    #     usr = input("사용자 입력(ID) : ")
    #     home_path = os.path.expanduser('~')     # home directory
    #     # print(home_path)

    #     path = home_path + '\\logfile'      # make logfile directory
    #     os.makedirs(path, exist_ok=True)
        
    #     hashed_usr = sha1_hash(usr)      # change user to hashed text
    #     print(hashed_usr)
    #     path += '\\'
    #     path += hashed_usr[:3]
        
    #     # directory 구조 : hashed_usr[0:2]/hashed_usr[3:]
    #     if os.path.isdir(path):     # check directory's exist
    #         path += '\\'
    #         path += hashed_usr[3:]
    #         if os.path.isdir(path):
    #             continue
    #         else:
    #             os.makedirs(path, exist_ok=True)
    #             break
        
    #     else:       # check directory's exist
    #         os.makedirs(path, exist_ok=True)    # make directory
    #         path += '\\'
    #         path += hashed_usr[3:]
    #         os.makedirs(path, exist_ok=True)    # make directory
    #         print(path)
    #         break

    print("\n기능 소개는 기능, ㄱㄴ을 입력하세요.\n")
    inp = ''        # 입력 정보를 담는 변수
    inp2 = ''       # 세부 입력 정보를 담는 변수
    randnum = 0     # 다양한 대답을 선택 할 난수를 담을 변수

    proc = mp.current_process()
    # print(proc.name)
    # print(proc.pid)

    while 1:
        #랜덤 변수를 통해서 대답 선택
        randnum = random.randint(1,4)
        if randnum == 1 :
            print("무엇을 도와드릴까요?")
        elif randnum == 2 :
            print("무엇이든 물어보세요!")
        elif randnum == 3 :
            print("어떤 것을 도와드려요?")
        else :
            print("무엇이든 말씀하세요!")

        inp = input()   # 기능 입력

        # function
        if '기능' in inp or 'ㄱㄴ' in inp:
            funcText()
        elif '오늘' in inp or 'ㅇㄴ' in inp or '오늘의 뉴스' in inp:
            today()
        elif '주간' in inp or 'ㅈㄱ' in inp:
            weekly()
        elif '검색' in inp or 'ㄱㅅ' in inp or 'ㄳ' in inp:
            search_key()
        elif '구글제로프로젝트' in inp:
            googlezero()
        elif '추천' in inp or 'ㅊㅊ' in inp:
            recommend()
        elif '종료' in inp or 'ㅈㄹ' in inp:
            print("이용해주셔서 감사합니다.")
            break
        # else
        else :
            if randnum == 1 :
                print("무슨 말씀이신지 잘 모르겠습니다.")
            elif randnum == 2 :
                print("무슨 뜻이에요? 혹시 좀 더 쉬운 단어가 있을까요?")
            elif randnum == 3 :
                print("아직 추가되지 않은 명령어입니다.")
            else :
                print("제가 모르는 명령어 입니다.")

######################################################################################################################################################


#################################################################### recommend news ####################################################################
### 여기 다시하기
def recommend():
    # 주말을 제외한 날짜
    # 설정한 시간에 메세지를 전달 (뉴스 전달 - 추천 뉴스)
    proc = mp.current_process()
    # print(proc.name)
    # print(proc.pid)

    # time.sleep(5)
    
    chk = 1

    while 1:
        d_today = datetime.datetime.now()   # date time (오늘 날짜)
        randnum = random.randint(1,2)
        if d_today.strftime('%a') != 'Sun' and d_today.strftime('%a') != 'Sat':     # 주말 제외
            if d_today.strftime('%H') == '08':      # 08:00 시간 설정
                # 보안뉴스 혹은 데일리시큐 랜덤 선택
                if chk == 1:
                    print("[오늘의 추천 뉴스]")
                    if randnum == 1:            # 보안뉴스
                        url_rec = "https://www.boannews.com/media/t_list.asp"
                        res = requests.get(url_rec, headers=headers)
                        res.raise_for_status()
                        soup = BeautifulSoup(res.text, "lxml")
                        headline = soup.find("div", attrs={"class":"news_list"})
                        print("<보안뉴스>")
                        title = headline.find("span", attrs={"class":"news_txt"}).get_text()
                        print(title)
                        link = "https://www.boannews.com/" + headline.find("a")["href"]
                        print(link)
                        chk = 0
                    else:                       # 데일리시큐
                        url_rec = "https://dailysecu.com/"
                        res = requests.get(url_rec, headers=headers)
                        res.raise_for_status()
                        soup = BeautifulSoup(res.text, "lxml")
                        headline = soup.find("li", attrs={"class":"clearfix"})
                        print("<데일리시큐>")
                        title = headline.find("strong").get_text()
                        print(title)
                        link = "https://dailysecu.com/" + headline.find("a")["href"]
                        print(link)
                        chk = 0
                    print()
            else:
                chk = 1

######################################################################################################################################################


#################################################################### today's news(or most recently news) ####################################################################
def today():
    print("[Today's News]\n")
    d_today = datetime.datetime.now()   # date time (오늘 날짜)
    translator = Translator()

    ### The Hacker News (https://thehackernews.com/) ###

    # dat = d_today.strftime('%B %d, %Y')
    dat = "July 20, 2021"       ### JUST FOR TEST
    # print(dat)

    url_hacker_news = "https://thehackernews.com/"                  ########## URL 확인하기 ###########
    res = requests.get(url_hacker_news, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"body-post clear"})     # get articles from 'thehackernews'

    print("<The Hacker News>")
    for idx, post in enumerate(posts):
        date_name = post.find("div", attrs={"class":"item-label"}).get_text() # 날짜 + 작성자
        print(date_name[1:len(dat)+1])
        if (dat != date_name[1:len(dat)+1]):            # same date (compare with today)
            if idx == 0:
                # 오늘의 뉴스 X
                print("The Hacker News 에서 오늘의 글이 없습니다.")
            break

        title = post.find("h2", attrs={"class":"home-title"}).get_text()            # title of the article
        # print(title)
        result = translator.translate(title, src='en', dest="ko")           # translate to korean
        print(result.text)

        link = post.find("a", attrs={"class":"story-link"})["href"]         # article's URL
        print(link)

        if idx > 1: break           # MAX = 3

    print()

    ### 보안 뉴스 (https://www.boannews.com/) ###
    url_kor = "https://www.boannews.com/media/t_list.asp"
    res = requests.get(url_kor, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"news_list"})       # get articles from '보안뉴스'

    dat = d_today.strftime("%Y년 %m월 %d일")
    # dat = "2021년 07월 06일"        ### JUST FOR TEST
    # print(dat)

    print("<보안뉴스>")
    for idx, post in enumerate(posts):
        date_name = post.find("span", attrs={"class":"news_writer"}).get_text() # 날짜
        s = date_name.find('|')
        date = date_name[s+2:len(date_name)-6]
        # print(date)
        if dat == date:         # same date
            title = post.find("span", attrs={"class":"news_txt"}).get_text()    # title of the article
            print(title)
            link = url_kor[0:len(url_kor)-17] + post.find("a")["href"]
            print(link)
        else:
            if idx == 0:
                # 오늘의 뉴스 X
                print("보안뉴스 에서 오늘의 글이 없습니다.")
            break

        if idx > 1: break       # MAX = 3

    print()

    # info security 사이트 내 문제 발생하여 보류
    """
    ### info security (https://www.infosecurity-magazine.com/) ###
    url_inse = "http://www.infosecurity-magazine.com/news/"
    res = requests.get(url_inse, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"webpage-item with-thumbnail"})

    dat = d_today.strftime("%#d %b %Y")
    # dat = "5 Jul 2021"          ### JUST FOR TEST
    # print(dat)

    print("<Info Security>")
    for idx, post in enumerate(posts):
        date = post.find("span", attrs={"class":"pub-date"}).get_text()
        # print(date)
        if date == dat:
            title = post.find("h3", attrs={"itemprop":"name"}).get_text()       # get title
            # print(title)
            result = translator.translate(title, src='en', dest="ko")           # translate title to korean
            print(result.text)

            link = post.a["href"]
            print(link)
        else:
            if idx == 0:
                # 오늘의 뉴스 X
                print("Info Security 에서 오늘의 글이 없습니다.")
            break

        if idx > 1:     # Max = 3
            break

    print()
    """

    # ( New 'News Website' )
    ### 데일리시큐 (https://www.dailysecu.com/) ###
    url_daily = "https://www.dailysecu.com/news/articleList.html?view_type=sm"
    res = requests.get(url_daily, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"list-block"})

    # dat = d_today.strftime('%Y-%m-%d')
    dat = "2021-07-11"
    print("<데일리시큐>")
    for idx, post in enumerate(posts):
        date = post.find("div", attrs={"class":"list-dated"}).get_text()
        # print(date[date.rfind('|')+2:-6])
        if dat == date[date.rfind('|')+2:-6]:
            title = post.find("strong").get_text()
            print(title)
            link = "https://www.dailysecu.com" + post.find("a")["href"]
            print(link)
        else: 
            if idx == 0:
                print("데일리시큐 에서 오늘의 글이 없습니다.")
            break
    print()

    ### WIRED (https://www.wired.com/) ###
    url_wired = "https://www.wired.com/most-recent/"
    res = requests.get(url_wired, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("li", attrs={"class":"archive-item-component"})

    # dat = d_today.strftime('%B %#d, %Y')
    dat = "July 11, 2021"
    print("<WIRED>")
    for post in posts:
        date = post.find("time").get_text()
        # print(date)
        if dat == date:
            title = post.find("h2", attrs={"class":"archive-item-component__title"}).get_text()
            # print(title)
            result = translator.translate(title, src='en', dest="ko")           # translate to korean
            print(result.text)
            link = "https://www.wired.com" + post.find("a")["href"]
            print(link)
        else:
            if idx == 0:
                print("Wired 에서 오늘의 글이 없습니다.")
            break
    print()

######################################################################################################################################################


#################################################################### weekly hot news (TOP3) ####################################################################
def weekly():
    print("[주간 HOT NEWS]\n")
    translator = Translator()

    ### The Hacker News (https://thehackernews.com/) ###
    url_hacker_news = "https://thehackernews.com/"
    res = requests.get(url_hacker_news, headers=headers)         # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"cf pop-article clear"})        # get articles from 'thehackernews'

    print("<The Hacker News>")
    for idx, post in enumerate(posts):
        title = post.find("div", attrs={"class":"pop-title"}).get_text()        # get title
        # print(title)
        result = translator.translate(title, src="en", dest="ko")               # translate title
        print(result.text)

        link = post.find("a", attrs={"class":"pop-link cf"})["href"]            # article's link
        print(link)

        if idx > 1:     # TOP 3
            break
    print()

    ### 보안 뉴스 (https://www.boannews.com/) ###
    url_kor = "https://www.boannews.com/media/o_list.asp"
    res = requests.get(url_kor, headers=headers)         # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"news_list"})     # get articles from 'thehackernews'

    print("<보안뉴스>")
    for idx, post in enumerate(posts):
        title = post.find("span", attrs={"class":"news_txt"}).get_text()        # article's title
        print(title)

        link = post.find("a")["href"]       # article's link
        print(url_kor[0:len(url_kor)-17]+link)

        if idx > 1:     # TOP 3
            break
    print()

    # info security 사이트 내 문제 발생하여 보류
    """
    ### info security (https://www.infosecurity-magazine.com/) ### ( New 'News Website' )
    url_inse = "https://www.infosecurity-magazine.com/news/"
    res = requests.get(url_inse, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"content-item content-sml whats-hot-item colour-news"})

    print("<Info Security>")
    for idx, post in enumerate(posts):
        title = post.find("h3", attrs={"class":"content-headline"}).get_text()  # get title
        # print(title)
        result = translator.translate(title, src='en', dest="ko")               # translate to korean
        print(result.text)

        link = post.a["href"]       # get link
        print(link)
        if idx > 1:     # TOP 3
            break
    print()
    """

    # ( New 'News Website' )
    ### 데일리시큐 (https://www.dailysecu.com/) ###
    url_daily = "https://www.dailysecu.com/news/articleList.html?view_type=sm"
    res = requests.get(url_daily, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("li", attrs={"class":"dis-table width-full auto-martop-14 auto-padtop-14 auto-sol"})

    print("<데일리시큐>")
    for idx, post in enumerate(posts):
        News = post.find("div", attrs={"class":"dis-table-cell"})
        title = News.find("a").get_text()       # get title
        print(title)
        link = "https://www.dailysecu.com/" + News.find("a")["href"]    # get link
        print(link)
        if idx > 1:     # TOP 3
            break
    print()

    ### 와이어드 (https://www.wired.com/most-recent/) ###
    url_wire = "https://www.wired.com/most-recent/"
    res = requests.get(url_wire, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("li", attrs={"class":"post-listing-list-item__post"})

    print("<WIRED>")
    for idx, post in enumerate(posts):
        title = post.find("h5", attrs={"class":"post-listing-list-item__title"}).get_text()       # get title
        # print(title)
        result = translator.translate(title, src='en', dest="ko")               # translate to korean
        print(result.text)
        link = post.find("a")["href"]    # get link
        print(link)
        if idx > 1:     # TOP 3
            break
    print()

#########################################################################################################################################################


#################################################################### Search Keyword ####################################################################
def search_key():
    strk = input("사용자 입력: ")    # 입력
    print("\nSearch\n")
    translator = Translator()

    # 영어로 입력시 그대로 서치.
    # 한글로 입력시 영어로 번역하여 서치. (X)
    # 모두 따로 search - 한글 입력 시 '보안 뉴스' 에서만 서칭.

    if strk.encode().isalpha():     # 영어 판단
        chk = 0
    else:
        chk = 1
    # headless Chrome setting
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')         # 보안성 주의
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    
    # browser driver settings
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)

    ### The Hacker News ###
    # browser = webdriver.Chrome(ChromeDriverManager().install())

    if chk == 0:
        print("<The Hacker News>")
        browser.get("https://cse.google.com/cse?q=&cx=partner-pub-7983783048239650%3A3179771210#gsc.tab=0&gsc.q={}&gsc.page=1".format(strk))
        browser.implicitly_wait(10)

        soup = BeautifulSoup(browser.page_source, "lxml")           # get from webdriver
        table = soup.find("div", attrs={"class":"gsc-resultsbox-visible"})
        posts = table.find_all("div", attrs={"class":"gsc-webResult gsc-result"})

        for idx, post in enumerate(posts):
            title = post.find("a", attrs={"class":"gs-title"})
            if title is None:
                if idx == 0:
                    print("검색된 결과가 없습니다.")
                break
            # print(title.get_text())
            result = translator.translate(title.get_text(), src="en", dest="ko")
            print(result.text)
            link = post.a["href"]
            print(link)
            if idx > 5:
                break
        print()

    ### 보안 뉴스 ###
    # browser = webdriver.Chrome(ChromeDriverManager().install())
    # browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    print("<보안뉴스>")
    browser.get("https://www.boannews.com/default.asp")

    browser.find_element_by_class_name("find").send_keys(strk)
    browser.find_element_by_class_name("find03").click()
    browser.implicitly_wait(10)

    soup = BeautifulSoup(browser.page_source, "lxml")           # get from webdriver
    table = soup.find("td", attrs={"align":"right", "valign":"top"})
    posts = table.find_all("tr")

    for idx, post in enumerate(posts):
        if idx % 2 == 1:
            continue
        title = post.find("span", attrs={"style":"font-size:14px;color:#1000CC;text-decoration:underline;line-height:25px;"})
        if title is None:
            if idx == 0:
                print("검색된 결과가 없습니다.")
            break
        print(title.get_text())

        link = post.a["href"]
        print("https://www.boannews.com"+link)
        # post = post.find_next_sibling("tr")
        if idx > 10:
            break
    print()

    # info security 사이트 내 문제 발생하여 보류
    """
    ### Info Security ###
    # browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    # browser = webdriver.PhantomJS(ChromeDriverManager().install())    # currently not using

    # Info Security 스크롤링 속도 늦음.

    if chk == 0:
        print("<Info Security>")
        browser.get("https://www.infosecurity-magazine.com/search/?q={}".format(strk))      # search key word

        # hide user agent
        # user_agent = driver.find_element_by_css_selector('#user-agent').text
        # print('User-Agent: ', user_agent)

        elem = browser.find_element_by_id("onetrust-accept-btn-handler")
        elem.click()
        browser.implicitly_wait(10)

        soup = BeautifulSoup(browser.page_source, "lxml")           # get from webdriver
        posts = soup.find_all("div", attrs={"class":"gsc-webResult gsc-result"})

        for idx, post in enumerate(posts):
            title = post.find("a", attrs={"class":"gs-title"})
            if title is None:
                if idx == 0:
                    print("검색된 결과가 없습니다.")
                break
            result = translator.translate(title.get_text(), src="en", dest="ko")
            print(result.text)
            link = post.a["href"]
            print(link)
            if idx > 5:
                break
        print()

    browser.quit()
    """

    ### 데일리시큐 ###
    # browser = webdriver.Chrome(ChromeDriverManager().install())
    # browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    print("<데일리시큐>")
    browser.get("https://www.dailysecu.com/")
    browser.find_element_by_id("search").click()
    browser.find_element_by_id("search").send_keys(strk)
    browser.find_element_by_xpath("//*[@id=\"user-nav\"]/fieldset/form/button").click()
    browser.implicitly_wait(10)

    soup = BeautifulSoup(browser.page_source, "lxml")           # get from webdriver
    posts = soup.find_all("div", attrs={"class":"list-block"})
    for idx, post in enumerate(posts):
        news = post.find("div", attrs={"class":"list-titles"})
        title = news.find("a")
        if title is None:
            if idx == 0:
                print("검색된 결과가 없습니다.")
            break
        print(title.get_text())
        link = post.a["href"]
        print("https://www.dailysecu.com"+link)
        if idx > 5:
            break
    print()


    ### WIRED ###
    # browser = webdriver.Chrome(ChromeDriverManager().install())
    # browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    if chk == 0:
        print("<WIRED>")
        url_wire = "https://www.wired.com/search/?q={}&page=1&sort=score".format(strk)
        res = requests.get(url_wire, headers=headers)         # check the request
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        posts = soup.find_all("li", attrs={"class":"archive-item-component"})
        for idx, post in enumerate(posts):
            title = post.find("h2", attrs={"class":"archive-item-component__title"})
            if title is None:
                if idx == 0:
                    print("검색된 결과가 없습니다.")
                break
            # print(title.get_text())
            result = translator.translate(title.get_text(), src="en", dest="ko")
            print(result.text)
            link = post.a["href"]
            print("https://www.wired.com/"+link)
            if idx > 5:
                break
        print()

    browser.quit()

    # # save in logfile
    # file_name = os.path.expanduser('~') + '\\logfile\\' + hashed_usr[:3] + '\\' + hashed_usr[3:] + '\\'
    # file_name += sha1_hash(strk)

    # if os.path.isfile(file_name):
    #     rfile = open(file_name, "r")    # read
    #     cnt = int(rfile.read()) + 1     # count해줌 (1 더함)
    #     rfile.close()

    #     t = open(file_name, "r+")   # write
    #     t.truncate(0)
    #     t.write(str(cnt))
    #     t.close()

    # else:
    #     wfile = open(file_name, "w")    # 파일 생성 및 1 더해줌
    #     wfile.write('1')
    #     wfile.close()

#########################################################################################################################################################


#################################################################### Google Zero Project ####################################################################
def googlezero():
    url_zero = "https://googleprojectzero.blogspot.com/"
    res = requests.get(url_zero, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    print("<Google Prject Zero>\n")
    print(url_zero)
#########################################################################################################################################################


# s()     # start


#################################################################### Configure the Update in website ####################################################################

# sched = BlockingScheduler()     # scheduler
# sched.add_job(작동시킬 함수명, 'interval', hours=1)
# # start
# sched.start()

# old_links = []

#########################################################################################################################################################


if __name__ == "__main__":
    # process spawning
    p = mp.Process(name="SubProcess", target=recommend)
    p.start()
    s()


#########################################################################################################################################################