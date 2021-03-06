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
# from flask import Flask                                       ### ????????? i ?????? ?????? ????????? ?????? import ????????? ?????? ????????? ??????
from bs4 import BeautifulSoup
from googletrans import Translator                              ########## googletrans?????? ???????????? ?????? ??? ??????. ?????? ?????? ?????? ##########
## ??? ???????????? ????????? ?????? ??????

from selenium import webdriver                                  ### ????????? (?????????????)
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
    #     date_name = post.find("div", attrs={"class":"item-label"}).get_text() # ?????? + ?????????
    #     if (dat != date_name[1:len(dat)+1]):            # same date (compare with today)
    #         break

    #     title = post.find("h2", attrs={"class":"home-title"}).get_text()            # title of the article
    #     # print(title)

    #     result = translator.translate(title, src='en', dest="ko")           # translate to korean
    #     print(result.text)

    #     link = post.find("a", attrs={"class":"story-link"})["href"]         # article's URL
    #     print(link)

    #     cnt += 1


########### (???) ???????????? ????????? ?????? ?????? ################
########### (??????) ??? ???????????? ??? ###############

##### Flask, Django -> ????????? i ?????? ?????? ?????? ??? ????????? (ver2, ver2_2)

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}

# translator = Translator()

#################################################################### show function ####################################################################

def funcText():
    print("-----------??????-----------")
    print("????????? ?????? ?????? : ??????, ??????, ????????? ??????\n")
    print("??? ?????? HOT ?????? ?????? : ??????, ??????\n")
    print("?????? ?????? ?????? : ??????, ??????, ???\n")
    print("??????'s ??????????????????: ????????????????????????\n")
    print("?????? ?????? : ??????, ??????\n")

######################################################################################################################################################


#################################################################### SHA1 ####################################################################
# ?????? ????????? ??????
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
    #     usr = input("????????? ??????(ID) : ")
    #     home_path = os.path.expanduser('~')     # home directory
    #     # print(home_path)

    #     path = home_path + '\\logfile'      # make logfile directory
    #     os.makedirs(path, exist_ok=True)
        
    #     hashed_usr = sha1_hash(usr)      # change user to hashed text
    #     print(hashed_usr)
    #     path += '\\'
    #     path += hashed_usr[:3]
        
    #     # directory ?????? : hashed_usr[0:2]/hashed_usr[3:]
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

    print("\n?????? ????????? ??????, ????????? ???????????????.\n")
    inp = ''        # ?????? ????????? ?????? ??????
    inp2 = ''       # ?????? ?????? ????????? ?????? ??????
    randnum = 0     # ????????? ????????? ?????? ??? ????????? ?????? ??????

    proc = mp.current_process()
    # print(proc.name)
    # print(proc.pid)

    while 1:
        #?????? ????????? ????????? ?????? ??????
        randnum = random.randint(1,4)
        if randnum == 1 :
            print("????????? ???????????????????")
        elif randnum == 2 :
            print("???????????? ???????????????!")
        elif randnum == 3 :
            print("?????? ?????? ????????????????")
        else :
            print("???????????? ???????????????!")

        inp = input()   # ?????? ??????

        # function
        if '??????' in inp or '??????' in inp:
            funcText()
        elif '??????' in inp or '??????' in inp or '????????? ??????' in inp:
            today()
        elif '??????' in inp or '??????' in inp:
            weekly()
        elif '??????' in inp or '??????' in inp or '???' in inp:
            search_key()
        elif '????????????????????????' in inp:
            googlezero()
        elif '??????' in inp or '??????' in inp:
            recommend()
        elif '??????' in inp or '??????' in inp:
            print("?????????????????? ???????????????.")
            break
        # else
        else :
            if randnum == 1 :
                print("?????? ??????????????? ??? ??????????????????.")
            elif randnum == 2 :
                print("?????? ????????????? ?????? ??? ??? ?????? ????????? ?????????????")
            elif randnum == 3 :
                print("?????? ???????????? ?????? ??????????????????.")
            else :
                print("?????? ????????? ????????? ?????????.")

######################################################################################################################################################


#################################################################### recommend news ####################################################################
### ?????? ????????????
def recommend():
    # ????????? ????????? ??????
    # ????????? ????????? ???????????? ?????? (?????? ?????? - ?????? ??????)
    proc = mp.current_process()
    # print(proc.name)
    # print(proc.pid)

    # time.sleep(5)
    
    chk = 1

    while 1:
        d_today = datetime.datetime.now()   # date time (?????? ??????)
        randnum = random.randint(1,2)
        if d_today.strftime('%a') != 'Sun' and d_today.strftime('%a') != 'Sat':     # ?????? ??????
            if d_today.strftime('%H') == '08':      # 08:00 ?????? ??????
                # ???????????? ?????? ??????????????? ?????? ??????
                if chk == 1:
                    print("[????????? ?????? ??????]")
                    if randnum == 1:            # ????????????
                        url_rec = "https://www.boannews.com/media/t_list.asp"
                        res = requests.get(url_rec, headers=headers)
                        res.raise_for_status()
                        soup = BeautifulSoup(res.text, "lxml")
                        headline = soup.find("div", attrs={"class":"news_list"})
                        print("<????????????>")
                        title = headline.find("span", attrs={"class":"news_txt"}).get_text()
                        print(title)
                        link = "https://www.boannews.com/" + headline.find("a")["href"]
                        print(link)
                        chk = 0
                    else:                       # ???????????????
                        url_rec = "https://dailysecu.com/"
                        res = requests.get(url_rec, headers=headers)
                        res.raise_for_status()
                        soup = BeautifulSoup(res.text, "lxml")
                        headline = soup.find("li", attrs={"class":"clearfix"})
                        print("<???????????????>")
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
    d_today = datetime.datetime.now()   # date time (?????? ??????)
    translator = Translator()

    ### The Hacker News (https://thehackernews.com/) ###

    # dat = d_today.strftime('%B %d, %Y')
    dat = "July 20, 2021"       ### JUST FOR TEST
    # print(dat)

    url_hacker_news = "https://thehackernews.com/"                  ########## URL ???????????? ###########
    res = requests.get(url_hacker_news, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"body-post clear"})     # get articles from 'thehackernews'

    print("<The Hacker News>")
    for idx, post in enumerate(posts):
        date_name = post.find("div", attrs={"class":"item-label"}).get_text() # ?????? + ?????????
        print(date_name[1:len(dat)+1])
        if (dat != date_name[1:len(dat)+1]):            # same date (compare with today)
            if idx == 0:
                # ????????? ?????? X
                print("The Hacker News ?????? ????????? ?????? ????????????.")
            break

        title = post.find("h2", attrs={"class":"home-title"}).get_text()            # title of the article
        # print(title)
        result = translator.translate(title, src='en', dest="ko")           # translate to korean
        print(result.text)

        link = post.find("a", attrs={"class":"story-link"})["href"]         # article's URL
        print(link)

        if idx > 1: break           # MAX = 3

    print()

    ### ?????? ?????? (https://www.boannews.com/) ###
    url_kor = "https://www.boannews.com/media/t_list.asp"
    res = requests.get(url_kor, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"news_list"})       # get articles from '????????????'

    dat = d_today.strftime("%Y??? %m??? %d???")
    # dat = "2021??? 07??? 06???"        ### JUST FOR TEST
    # print(dat)

    print("<????????????>")
    for idx, post in enumerate(posts):
        date_name = post.find("span", attrs={"class":"news_writer"}).get_text() # ??????
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
                # ????????? ?????? X
                print("???????????? ?????? ????????? ?????? ????????????.")
            break

        if idx > 1: break       # MAX = 3

    print()

    # info security ????????? ??? ?????? ???????????? ??????
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
                # ????????? ?????? X
                print("Info Security ?????? ????????? ?????? ????????????.")
            break

        if idx > 1:     # Max = 3
            break

    print()
    """

    # ( New 'News Website' )
    ### ??????????????? (https://www.dailysecu.com/) ###
    url_daily = "https://www.dailysecu.com/news/articleList.html?view_type=sm"
    res = requests.get(url_daily, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"list-block"})

    # dat = d_today.strftime('%Y-%m-%d')
    dat = "2021-07-11"
    print("<???????????????>")
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
                print("??????????????? ?????? ????????? ?????? ????????????.")
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
                print("Wired ?????? ????????? ?????? ????????????.")
            break
    print()

######################################################################################################################################################


#################################################################### weekly hot news (TOP3) ####################################################################
def weekly():
    print("[?????? HOT NEWS]\n")
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

    ### ?????? ?????? (https://www.boannews.com/) ###
    url_kor = "https://www.boannews.com/media/o_list.asp"
    res = requests.get(url_kor, headers=headers)         # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"news_list"})     # get articles from 'thehackernews'

    print("<????????????>")
    for idx, post in enumerate(posts):
        title = post.find("span", attrs={"class":"news_txt"}).get_text()        # article's title
        print(title)

        link = post.find("a")["href"]       # article's link
        print(url_kor[0:len(url_kor)-17]+link)

        if idx > 1:     # TOP 3
            break
    print()

    # info security ????????? ??? ?????? ???????????? ??????
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
    ### ??????????????? (https://www.dailysecu.com/) ###
    url_daily = "https://www.dailysecu.com/news/articleList.html?view_type=sm"
    res = requests.get(url_daily, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("li", attrs={"class":"dis-table width-full auto-martop-14 auto-padtop-14 auto-sol"})

    print("<???????????????>")
    for idx, post in enumerate(posts):
        News = post.find("div", attrs={"class":"dis-table-cell"})
        title = News.find("a").get_text()       # get title
        print(title)
        link = "https://www.dailysecu.com/" + News.find("a")["href"]    # get link
        print(link)
        if idx > 1:     # TOP 3
            break
    print()

    ### ???????????? (https://www.wired.com/most-recent/) ###
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
    strk = input("????????? ??????: ")    # ??????
    print("\nSearch\n")
    translator = Translator()

    # ????????? ????????? ????????? ??????.
    # ????????? ????????? ????????? ???????????? ??????. (X)
    # ?????? ?????? search - ?????? ?????? ??? '?????? ??????' ????????? ??????.

    if strk.encode().isalpha():     # ?????? ??????
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
    chrome_options.add_argument('--no-sandbox')         # ????????? ??????
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
                    print("????????? ????????? ????????????.")
                break
            # print(title.get_text())
            result = translator.translate(title.get_text(), src="en", dest="ko")
            print(result.text)
            link = post.a["href"]
            print(link)
            if idx > 5:
                break
        print()

    ### ?????? ?????? ###
    # browser = webdriver.Chrome(ChromeDriverManager().install())
    # browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    print("<????????????>")
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
                print("????????? ????????? ????????????.")
            break
        print(title.get_text())

        link = post.a["href"]
        print("https://www.boannews.com"+link)
        # post = post.find_next_sibling("tr")
        if idx > 10:
            break
    print()

    # info security ????????? ??? ?????? ???????????? ??????
    """
    ### Info Security ###
    # browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    # browser = webdriver.PhantomJS(ChromeDriverManager().install())    # currently not using

    # Info Security ???????????? ?????? ??????.

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
                    print("????????? ????????? ????????????.")
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

    ### ??????????????? ###
    # browser = webdriver.Chrome(ChromeDriverManager().install())
    # browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    print("<???????????????>")
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
                print("????????? ????????? ????????????.")
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
                    print("????????? ????????? ????????????.")
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
    #     cnt = int(rfile.read()) + 1     # count?????? (1 ??????)
    #     rfile.close()

    #     t = open(file_name, "r+")   # write
    #     t.truncate(0)
    #     t.write(str(cnt))
    #     t.close()

    # else:
    #     wfile = open(file_name, "w")    # ?????? ?????? ??? 1 ?????????
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
# sched.add_job(???????????? ?????????, 'interval', hours=1)
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