from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
# from googletrans import Translator

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}

def week_boan():
    url = "https://www.boannews.com/media/o_list.asp"
    res = requests.get(url, headers=headers)         # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"news_list"})     # get articles from 'thehackernews'
    list = []
    for idx, post in enumerate(posts):
        title = post.find("span", attrs={"class":"news_txt"}).get_text()        # article's title
        date = post.find("span", attrs={"class":"news_writer"}).get_text()
        img = "https://lh3.googleusercontent.com/proxy/1LmiZPdyXzxkMydjribuQFpejVfaARtYU3AzTnukgGQuWm6IrfhRal-3mZxTvRxGQXOrwI58bUHaiFlh5jkbHxrQPsBwCia0O7Sr-ZA_5wjx0Q"
        if post.find("img") != None:
            img = post.find("img")["src"]
            img = "https://www.boannews.com/" + img

        link = "https://www.boannews.com" + post.find("a")["href"]       # article's link
        list.append((title, date, img, link))

        if idx >= 4:
            break
    return list

def week_daily():
    url = "https://www.dailysecu.com/news/articleList.html?view_type=sm"
    res = requests.get(url, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("li", attrs={"class":"dis-table width-full auto-martop-14 auto-padtop-14 auto-sol"})
    list = []

    first = soup.find("li", attrs={"class":"dis-table width-full"})
    title = first.find("a").get_text()
    img = first.find("a", attrs={"class":"dis-table-cell auto-images cover line width-114 height-80 auto-marleft-14"})["style"]
    img = "https://dailysecu.com" + img[21:-1]
    link = "https://dailysecu.com" + first.find("a")["href"]
    list.append((title, img, link))

    for idx, post in enumerate(posts):
        title = post.find("a").get_text()
        img = "https://lh3.googleusercontent.com/proxy/1LmiZPdyXzxkMydjribuQFpejVfaARtYU3AzTnukgGQuWm6IrfhRal-3mZxTvRxGQXOrwI58bUHaiFlh5jkbHxrQPsBwCia0O7Sr-ZA_5wjx0Q"
        if post.find("a", attrs={"class":"dis-table-cell auto-images cover line width-114 height-80 auto-marleft-14"}) != None:
            img = post.find("a", attrs={"class":"dis-table-cell auto-images cover line width-114 height-80 auto-marleft-14"})["style"]
        img = "https://dailysecu.com" + img[21:-1]
        link = "https://dailysecu.com" + post.find("a")["href"]
        list.append((title, img, link))
    return list

def week_hacker():
    url = "https://thehackernews.com/"
    res = requests.get(url, headers=headers)         # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("div", attrs={"class":"cf pop-article clear"})        # get articles from 'thehackernews'
    list = []

    for idx, post in enumerate(posts):
        title = post.find("div", attrs={"class":"pop-title"}).get_text()
        img = post.find("img")["data-src"]
        link = post.find("a", attrs={"class":"pop-link cf"})["href"]
        list.append((title, img, link))
        if idx >= 4:
            break
    return list

def week_wired():
    url = "https://www.wired.com/most-popular/"
    res = requests.get(url, headers=headers)               # check the request
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    posts = soup.find_all("li", attrs={"class":"archive-item-component"})
    list = []

    for idx, post in enumerate(posts):
        title = post.find("h2", attrs={"class":"archive-item-component__title"}).get_text()       # get title
        date = post.find("time").get_text() + '  |  ' + post.find("a", attrs={"class":"byline-component__link"}).get_text()
        img = post.find("img")["src"]
        link = post.find("a")["href"]    # get link
        list.append((title, date, img, link))
        if idx >= 4:
            break
    return list