from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from urllib import parse
import requests

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}

def search_boan(wrd):
    ## encoding
    # print(wrd)
    if wrd.encode().isalpha():        # 영어
        word = wrd
        # print(word)
    else:                             # 한글
        word = parse.quote(wrd, encoding='euc-kr')
        # print(word)

    url = "https://www.boannews.com/search/news_total.asp?search=title&find={}".format(word)
    res = requests.get(url, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"news_list"})
    # print(posts)
    add_url = "https://m.boannews.com/html/search_all.html?search={}".format(wrd)
    list = []
    list.append(add_url)
    for i, post in enumerate(posts):
        title = post.find("span", attrs={"class":"news_txt"}).get_text()    # title of the article
        date = post.find("span", attrs={"class":"news_writer"}).get_text() # 날짜
        img = "https://lh3.googleusercontent.com/proxy/1LmiZPdyXzxkMydjribuQFpejVfaARtYU3AzTnukgGQuWm6IrfhRal-3mZxTvRxGQXOrwI58bUHaiFlh5jkbHxrQPsBwCia0O7Sr-ZA_5wjx0Q"
        if post.find("img") != None:
            img = "https://www.boannews.com" + post.find("img")["src"]
        link = "https://www.boannews.com" + post.find("a")["href"]
        list.append((title, date, img, link))

        if i >= 4:
            break
    return list

def search_daily(wrd):
    # print(wrd)
    
    url = "https://www.dailysecu.com/news/articleList.html?view_type=sm&sc_area=A&view_type=sm&sc_word={}".format(wrd)
    # print(url)
    res = requests.get(url, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"list-block"})
    list = []
    list.append(url)
    for i, post in enumerate(posts):
        title = post.find("strong").get_text()
        date = post.find("div", attrs={"class":"list-dated"}).get_text()
        img = "https://lh3.googleusercontent.com/proxy/1LmiZPdyXzxkMydjribuQFpejVfaARtYU3AzTnukgGQuWm6IrfhRal-3mZxTvRxGQXOrwI58bUHaiFlh5jkbHxrQPsBwCia0O7Sr-ZA_5wjx0Q"
        if post.find("div", attrs={"class":"list-image"}) != None:
            img = post.find("div", attrs={"class":"list-image"})["style"]
            img = "https://dailysecu.com/news" + img[22:-1]
        link = "https://www.dailysecu.com" + post.find("a")["href"]
        list.append((title, date, img, link))
        if i >= 4:
            break
    return list

### 보류 ###
def search_hacker(wrd):        # consideer using it
    # print(wrd)
    url = "https://cse.google.com/cse?cx=partner-pub-7983783048239650%3A3179771210#gsc.tab=0&gsc.q={}&gsc.sort=".format(wrd)
    
    res = requests.get(url, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"gsc-webResult gsc-result"})
    # print(posts)
    list = []
    list.append(url)
    cnt=0
    for post in posts:
        title = post.find("a", attrs={"class":"gs-title"}).get_text()
        t = post.find("div", attrs={"class":"gs-bidi-start-align gs-snippet"}).get_text()
        pos = t.find('.')
        date = t[:pos]
        img = post.find("img", attrs={"class":"gs-image"})["src"]
        link = post.find("a", attrs={"class":"gs-image"})["href"]
        list.append((title, date, img, link))
        cnt+=1
        if cnt >= 4:
            break
    return list

def search_wired(wrd):
    # print(wrd)
    url = "https://www.wired.com/search/?q={}&page=1&sort=score".format(wrd)
    res = requests.get(url, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("li", attrs={"class":"archive-item-component"})
    list = []
    list.append(url)
    i=0
    for post in posts:
        title = post.find("h2", attrs={"class":"archive-item-component__title"}).get_text()
        
        if post.find("time") == None:
            continue
        date = post.find("time").get_text()
        date += " | "
        date += post.find("a", attrs={"class":"byline-component__link"}).get_text()
        # print(i, " ", date)
        img = post.find("img")["src"]
        link = "https://www.wired.com" + post.find("a")["href"]
        list.append((title, date, img, link))
        i+=1
        if i > 4:
            break
    return list

def get_list(idx, wrd):
    if idx == 0:
        return search_boan(wrd)

    elif idx == 1:
        return search_daily(wrd)

    elif idx == 2:
        return search_wired(wrd)
    
    elif idx == 3:                ### 보류
        return search_hacker(wrd)