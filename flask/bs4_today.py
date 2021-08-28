# -*- encoding: utf-8 -*
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
# from googletrans import Translator

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}

def today_hacker():        # The Hacker News
    url = "https://thehackernews.com/"
    # translator = Translator()
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"body-post clear"})
    list = []
    for idx, post in enumerate(posts):
        title = post.find("h2", attrs={"class":"home-title"}).get_text()            # title of the article
        # result = translator.translate(title, src='en', dest="ko")
        date = post.find("div", attrs={"class":"item-label"}).get_text()
        link = post.find("a", attrs={"class":"story-link"})["href"]         # article's URL
        img = post.find("img", attrs={"alt":title})["data-src"]
        list.append((title, date[1:], img, link))
        
        # if idx >= 4: break
    return list

def today_boan():        # 보안 뉴스
    url = "https://www.boannews.com/media/t_list.asp"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"news_list"})       # get articles from '보안뉴스'
    list = []
    for idx, post in enumerate(posts):
        title = post.find("span", attrs={"class":"news_txt"}).get_text()    # title of the article
        date = post.find("span", attrs={"class":"news_writer"}).get_text() # 날짜
        img = "https://lh3.googleusercontent.com/proxy/1LmiZPdyXzxkMydjribuQFpejVfaARtYU3AzTnukgGQuWm6IrfhRal-3mZxTvRxGQXOrwI58bUHaiFlh5jkbHxrQPsBwCia0O7Sr-ZA_5wjx0Q"
        if post.find("img") != None:
            img = url[0:len(url)-17] + post.find("img")["src"]
        link = "https://www.boannews.com" + post.find("a")["href"]
        list.append((title, date, img, link))
        
        # if idx >= 4: break
    return list

def today_daily():        # 데일리시큐
    url = "https://www.dailysecu.com/news/articleList.html?view_type=sm"
    res = requests.get(url, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"list-block"})
    list = []
    for idx, post in enumerate(posts):
        title = post.find("strong").get_text()
        date = post.find("div", attrs={"class":"list-dated"}).get_text()
        
        img = "https://lh3.googleusercontent.com/proxy/1LmiZPdyXzxkMydjribuQFpejVfaARtYU3AzTnukgGQuWm6IrfhRal-3mZxTvRxGQXOrwI58bUHaiFlh5jkbHxrQPsBwCia0O7Sr-ZA_5wjx0Q"
        if post.find("div", attrs={"class":"list-image"}) != None:
            img = post.find("div", attrs={"class":"list-image"})["style"]
            img = "https://dailysecu.com/news" + img[22:-1]
        # else:
        #     idx -= 1
        #     continue
        
        link = "https://www.dailysecu.com" + post.find("a")["href"]
        list.append((title, date, img, link))
        
        # if idx >= 4: break
    return list

def today_wired():        # 와이어드
    url = "https://www.wired.com/most-recent/"
    res = requests.get(url, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("li", attrs={"class":"archive-item-component"})
    list = []
    for idx, post in enumerate(posts):
        title = post.find("h2", attrs={"class":"archive-item-component__title"}).get_text()
        date = post.find("time").get_text()
        date += " | "
        date += post.find("a", attrs={"class":"byline-component__link"}).get_text()
        img = post.find("img")["src"]
        link = "https://www.wired.com" + post.find("a")["href"]
        list.append((title, date, img, link))
    return list