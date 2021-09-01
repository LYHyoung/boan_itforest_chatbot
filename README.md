# Security Kakao Chatbot

### Ref.
+ Security Company : [ITForest](http://www.itforest.net/)  
+ Click [here](https://pf.kakao.com/_xfXbxeK) to find out about chatbot

### About
> This chatbot can scrap recent and weekly hot news about security issue's in ['보안뉴스'](https://www.boannews.com/default.asp?direct=mobile), ['데일리시큐'](https://www.dailysecu.com/), ['Wired'](https://www.wired.com/) and ['The Hacker News'](https://thehackernews.com/)  
> Also can get news issues by insert keyword like [Zero-Day](https://ko.wikipedia.org/wiki/%EC%A0%9C%EB%A1%9C_%EB%8D%B0%EC%9D%B4_%EA%B3%B5%EA%B2%A9) and [SolarWinds](https://www.solarwinds.com/ko/)

### ARCH.
<img src="https://user-images.githubusercontent.com/37611500/131669848-2d7c79ed-f9d6-4134-8082-312600872a3e.png">
> Server : AWS EC2

### DB Log Structure
> / : Directory  
> (None) : File

<pre>
<code>
/root
├── /admin
│   ├── Searched Word
│   ├── /_search
│   │   ├── 보안뉴스
│   │   ├── 데일리시큐
│   │   ├── The Hacker News
│   │   └── Wired
│   ├── /_recent
│   │   ├── 보안뉴스
│   │   ├── 데일리시큐
│   │   ├── The Hacker News
│   │   └── Wired
│   └── /_weekly
│       ├── 보안뉴스
│       ├── 데일리시큐
│       ├── The Hacker News
│       └── Wired
└── /Users
    ├── /userkey(hash[0:2])
    │   ├── /userkey(hash[3:])
    │   │   ├── user
    │   │   ├── SearchN 
    │   │   └──  /searched 
    │   │        └── Searched Word
...
    │   └── /userkey(hash[3:])
    │       └── ...
...
    └── /userkey(hash[0:2])
        └── ...
</code>
</pre>
