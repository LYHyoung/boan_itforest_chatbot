# -*- encoding: utf-8 -*
from flask import Flask, request, jsonify, render_template
import time
import json
import os
import datetime
import requests
import shutil
from bs4_today import *
from bs4_week import *
from bs4_search import *
# from bs4_rec import *
from makefiles import *
from sel_ipcheck import *

import threading

news_list = ['보안뉴스', '데일리시큐', 'Wired']

application = Flask(__name__)

# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}

@application.route("/start")
def hello():
    return "Hello Goorm"

@application.route("/option",methods=['POST'])
def option():
    req = request.get_json()

    answer = req["userRequest"]["utterance"]

    # IP를 읽어온다. 이후 IP에 맞는 해시값으로 변환하여 디렉토리 생성 후 정보들을 수집 (검색어 로깅, 검색하고자 하는 웹사이트 저장)
    ### get home directory path
    path = os.path.expanduser("~") + '/logfile'       # 첫번째 path 는 항상 homedirectory로 고정
    # make log directory
    # path += '/logfile'

    if os.path.isdir(path) is False:
        makedir_admin(path)

    cli = req["userRequest"]["user"]["properties"]["botUserKey"]    # client userkey 가져오기
    clipath = path + '/Users/' + cli[:3] + '/' + cli[3:]            # client path
    if os.path.isdir(clipath) is False:
        makedir_user(path, clipath)

    answer = answer.strip('\n')    # 컴퓨터에서 enter키 입력시 추가되는 개행 제거

    f = open(clipath + '/user', 'r')    # user내 이름이 비어있는지 확인 (비어 있다면 유저명 변경 옵션)
    s = f.read()
    s_t = "1"
    if os.path.isfile(clipath + '/AddFunc'):
        f_t = open(clipath + '/AddFunc', 'r')
        s_t = f_t.read()


#################################################################### 유저명 변경 완료 ####################################################################
    if s == "":        # 유저 명 변경
        f = open(clipath +'/user', 'w+t')
        f.write(answer)
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer + " (으)로 변경되었습니다."
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "messageText": "메뉴",
                        "action": "message",
                        "label": "메뉴"
                    }
                ]
            }
        }
#########################################################################################################################################################


#################################################################### IP 확인 ####################################################################
    elif s_t == "":
        f = open(clipath + '/AddFunc', 'w+t')
        f.write('2')

        threads = []
        t = threading.Thread(target=get_virustotal, args=(answer))
        t.start()
        threads.append(t)

        def set_text():
            re
        t2 = threading.Thread()

        soup_2_text = get_virustotal(answer)        # get IP/Domain detection from virus total

        if soup_2_text == "None":
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "No matches found"
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "messageText": "메뉴",
                            "action": "message",
                            "label": "메뉴"
                        }
                    ]
                }
            }
        else:
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": soup_2_text
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "messageText": "메뉴",
                            "action": "message",
                            "label": "메뉴"
                        }
                    ]
                }
            }
#########################################################################################################################################################


#################################################################### 시작 ####################################################################
    elif answer == "시작":
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": "인더포레스트 챗봇입니다",
                            "description": "메뉴를 눌러 시작해보세요 😸",
                            "thumbnail": {
                                "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/4.PNG"
                            }
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "messageText": "메뉴",
                        "action": "message",
                        "label": "메뉴"
                    }
                ]
            }
        }
#########################################################################################################################################################


#################################################################### 메뉴 ####################################################################
    elif answer == "메뉴" or answer == 'ㅁㄴ':
        f = open(clipath + '/user', 'r')
        user_num = f.read()
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "안녕하세요 " + user_num + " 님 😺😸\n\n인더포레스트 챗봇을 이용해주셔서 감사합니다!\n무엇을 도와드릴까요?"
                        }
                    },
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": [
                                {
                                    "title": "최근 뉴스",
                                    "description": user_num + " 님. 업데이트된 최신 보안 뉴스를 보여드립니다",
                                    "thumbnail": {
                                        "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/2.PNG"
                                    },
                                    "buttons": [
                                        {
                                            "action": "message",
                                            "label": "보안뉴스로 열기",
                                            "messageText": "보안뉴스's 최근"
                                        },
                                        {
                                            "action": "message",
                                            "label": "데일리시큐로 열기",
                                            "messageText": "데일리시큐's 최근"
                                        },
                                        {
                                            "action": "message",
                                            "label": "Wired로 열기",
                                            "messageText": "Wired's 최근"
                                        }
                                    ]
                                },
                                {
                                    "title": "주간 HOT 뉴스",
                                    "description": user_num + " 님. 주간 인기있는 보안 뉴스를 보여드립니다",
                                    "thumbnail": {
                                        "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/logo4.PNG"
                                    },
                                    "buttons": [
                                        {
                                            "action": "message",
                                            "label": "보안뉴스로 열기",
                                            "messageText": "보안뉴스's 주간"
                                        },
                                        {
                                            "action": "message",
                                            "label": "데일리시큐로 열기",
                                            "messageText": "데일리시큐's 주간"
                                        },
                                        {
                                            "action": "message",
                                            "label": "Wired로 열기",
                                            "messageText": "Wired's 주간"
                                        }
                                    ]
                                },
                                {
                                    "title": "뉴스 추천 + The Hacker News",
                                    "description": "추가된 사이트 및 검색 데이터를 분석하여 뉴스를 추천해드립니다",
                                    "thumbnail": {
                                        "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/2.PNG"
                                    },
                                    "buttons": [
                                        {
                                            "action": "message",
                                            "messageText": "뉴스 추천",
                                            "label": "뉴스 추천"
                                        },
                                        {
                                            "action": "message",
                                            "label": "더해커스뉴스 주간",
                                            "messageText": "The Hacker News's 주간"
                                        },
                                        {
                                            "action": "message",
                                            "label": "더해커스뉴스 최근",
                                            "messageText": "The Hacker News's 최근"
                                        }
                                    ]
                                },
                                {
                                    "title": "검색 사이트 설정",
                                    "description": user_num + " 님. 검색어 입력시 이용할 뉴스 사이트를 설정해주세요",
                                    "thumbnail": {
                                        "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/logo4.PNG"
                                    },
                                    "buttons": [
                                        {
                                            "action": "message",
                                            "label": "보안뉴스로 설정",
                                            "messageText": "보안뉴스로 설정"
                                        },
                                        {
                                            "action": "message",
                                            "label": "데일리시큐로 설정",
                                            "messageText": "데일리시큐로 설정"
                                        },
                                        {
                                            "action": "message",
                                            "label": "Wired로 설정",
                                            "messageText": "Wired로 설정"
                                        }
                                    ]
                                },
                                {
                                    "title": "인더포레스트 챗봇 v2.0",
                                    "description": "안녕하세요 " + user_num + " 님! 😸",
                                    "thumbnail": {
                                        "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/logo5.png"
                                    },
                                    "buttons": [
                                        {
                                            "label": "ABOUT US",
                                            "action": "webLink",
                                            "webLinkUrl": "http://www.itforest.net/company.php"
                                        },
                                        {
                                            "label": "이름(유저명) 바꾸기",
                                            "action": "message",
                                            "messageText": "유저명 변경하기"
                                        },
                                        {
                                            "label": "제공되는 뉴스 사이트 보기",
                                            "action": "message",
                                            "messageText": "뉴스 사이트 바로가기"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }
        }
#########################################################################################################################################################


#################################################################### ip 보안성 확인 ####################################################################
    elif answer == "IPHackedCheckTest":
        if os.path.isfile(clipath + '/AddFunc'):    # '~/AddFunc' 파일 유무 확인
            f = open(clipath + '/AddFunc', 'w+t')   # 내용 지움
            res = {
                "version": "2.0",
                "template": {
                    "outputs":  [
                        {
                            "simpleText": {
                                "text": "IP 혹은 도메인 주소를 입력해주세요"
                            }
                        }
                    ]
                }
            }
        else:
            res = {
              "version": "2.0",
              "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "검색 결과가 없습니다 ㅋ."
                        }
                    }
                ],
                "quickReplies": [
                  {
                    "messageText": "메뉴",
                    "action": "message",
                    "label": "메뉴"
                  }
                ]
              }
            }
#########################################################################################################################################################


#################################################################### 이름 바꾸기 ####################################################################
    elif answer == "유저명 변경하기":
        f = open(clipath + '/user', 'w+t')
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "유저명 변경을 도와드리겠습니다\n어떤 이름(User명)으로 변경하시겠습니까?"
                        }
                    }
                ]
            }
        }
#########################################################################################################################################################


#################################################################### 웹사이트 ####################################################################
    elif answer == "뉴스 사이트 바로가기":
        res = {
          "version": "2.0",
          "template": {
            "outputs": [
              {
                "listCard": {
                  "header": {
                    "title": "뉴스/웹 사이트"
                  },
                  "items": [
                    {
                      "title": "The Hacker News",
                      "description": "컴퓨터 과학과 기업가정신에 초점을 맞춘 소셜 뉴스 웹사이트",
                      "imageUrl": "https://media-exp3.licdn.com/dms/image/C510BAQH3yOT7M_sJ_w/company-logo_200_200/0/1579094827297?e=2159024400&v=beta&t=MrH8vVZjXRt707RMpAl4u_8hBedIaO4DlhTPWNAZaSA",
                      "link": {
                        "web": "https://thehackernews.com/"
                      }
                    },
                    {
                      "title": "보안뉴스",
                      "description": "국내 보안 언론/커뮤니티",
                      "imageUrl": "http://www.boannews.com/images/top/boannews_ci.png",
                      "link": {
                        "web": "https://www.boannews.com/media/t_list.asp"
                      }
                    },
                    {
                      "title": "데일리시큐",
                      "description": "국내 정보보안 및 IT 전문 언론",
                      "imageUrl": "https://m.euyira.com/web/product/big/201711/80_shop1_223037.jpg",
                      "link": {
                        "web": "https://dailysecu.com/news/articleList.html?view_type=sm"
                      }
                    },
                    {
                      "title": "WIRED",
                      "description": "미국 내 신흥 기술의 영향을 담은 잡지",
                      "imageUrl": "https://pbs.twimg.com/profile_images/1166701357702795264/rhyCnbTC_400x400.jpg",
                      "link": {
                        "web": "https://www.wired.com/most-recent/"
                      }
                    },
                    {
                      "title": "ITForest 바로가기",
                      "description": "인더포레스트\n Cyber Security ‘In The Forest’",
                      "imageUrl": "https://l.incru.it/2021/05/%EC%9D%B8%EB%8D%94%ED%8F%AC%EB%A0%88%EC%8A%A4%ED%8A%B8_Logo_20215271609.JPG",
                      "link": {
                        "web": "http://itforest.net/"
                      }
                    }
                  ]
                }
              }
            ],
            "quickReplies": [
              {
                "messageText": "메뉴",
                "action": "message",
                "label": "메뉴"
              }
            ]
          }
        }
#########################################################################################################################################################


#################################################################### 오늘의 뉴스 ####################################################################
    elif answer == "보안뉴스's 최근":
        adpath = path + '/admin/_recent/보안뉴스'
        f = open(adpath, 'r')
        N = int(f.read())
        f = open(adpath, 'w+t')
        f.write(str(N + 1))
        
        b_list = today_boan()        # 보안뉴스

        j_list = []
        for i in range(5):
            j_list.append({
                "title": b_list[i][0],
                "description": b_list[i][1],
                "imageUrl": b_list[i][2],
                "link": {
                    "web": b_list[i][3]
                }
            })

        res = {
          "version": "2.0",
          "template": {
            "outputs": [
              {
                  "listCard": {
                      "header": {
                          "title": answer
                      },
                      "items": j_list,
                      "buttons": [
                          {
                              "label": "더보기",
                              "action": "webLink",
                              "webLinkUrl": "https://m.boannews.com/html/news.html?mtype=1&tab_type=1"
                          }
                      ]
                  }
              }
            ],
            "quickReplies": [
              {
                "messageText": "메뉴",
                "action": "message",
                "label": "메뉴"
              }
            ]
          }
        }

    elif answer == "데일리시큐's 최근":
        adpath = path + '/admin/_recent/데일리시큐'
        f = open(adpath, 'r')
        N = int(f.read())
        f = open(adpath, 'w+t')
        f.write(str(N + 1))
        
        d_list = today_daily()        # 데일리시큐

        j_list = []
        for i in range(5):
            j_list.append({
                "title": d_list[i][0],
                "description": d_list[i][1],
                "imageUrl": d_list[i][2],
                "link": {
                    "web": d_list[i][3]
                }
            })

        res = {
          "version": "2.0",
          "template": {
            "outputs": [
              {
                "listCard": {
                      "header": {
                          "title": answer
                      },
                      "items": j_list,
                      "buttons": [
                          {
                              "label": "더보기",
                              "action": "webLink",
                              "webLinkUrl": "https://dailysecu.com/news/articleList.html?view_type=sm"
                          }
                      ]
                  }
              }
            ],
            "quickReplies": [
              {
                "messageText": "메뉴",
                "action": "message",
                "label": "메뉴"
              }
            ]
          }
        }
    elif answer == "The Hacker News's 최근":
        adpath = path + '/admin/_recent/The Hacker News'
        f = open(adpath, 'r')
        N = int(f.read())
        f = open(adpath, 'w+t')
        f.write(str(N + 1))

        h_list = today_hacker()    # The Hacker News

        j_list = []
        for i in range(5):
            j_list.append({
                "title": h_list[i][0],
                "description": h_list[i][1],
                "imageUrl": h_list[i][2],
                "link": {
                    "web": h_list[i][3]
                }
            })

        res = {
          "version": "2.0",
          "template": {
            "outputs": [
              {
                  "listCard": {
                      "header": {
                          "title": answer
                      },
                      "items": j_list,
                      "buttons": [
                          {
                              "label": "더보기",
                              "action": "webLink",
                              "webLinkUrl": "https://thehackernews.com/"
                          }
                      ]
                  }
              }
            ],
            "quickReplies": [
              {
                "messageText": "메뉴",
                "action": "message",
                "label": "메뉴"
              }
            ]
          }
        }
    elif answer == "Wired's 최근":
        adpath = path + '/admin/_recent/Wired'
        f = open(adpath, 'r')
        N = int(f.read())
        f = open(adpath, 'w+t')
        f.write(str(N + 1))
        
        w_list = today_wired()    # Wired + "의 뉴스"

        j_list = []
        for i in range(5):
            j_list.append({
                "title": w_list[i][0],
                "description": w_list[i][1],
                "imageUrl": w_list[i][2],
                "link": {
                    "web": w_list[i][3]
                }
            })

        res = {
          "version": "2.0",
          "template": {
            "outputs": [
              {
                  "listCard": {
                      "header": {
                          "title": answer
                      },
                      "items": j_list,
                      "buttons": [
                          {
                              "label": "더보기",
                              "action": "webLink",
                              "webLinkUrl": "https://www.wired.com/most-recent/"
                          }
                      ]
                  }
              }
            ],
            "quickReplies": [
              {
                "messageText": "메뉴",
                "action": "message",
                "label": "메뉴"
              }
            ]
          }
        }
#########################################################################################################################################################


#################################################################### 주간 HOT 뉴스 ####################################################################
    # 보안뉴스
    elif answer == "보안뉴스's 주간":
        adpath = path + '/admin/_weekly/보안뉴스'
        f = open(adpath, 'r')
        N = int(f.read())
        f = open(adpath, 'w+t')
        f.write(str(N + 1))
        
        b_list = week_boan()

        j_list = []
        for i in range(5):
            j_list.append({
                "title": b_list[i][0],
                "description": b_list[i][1],
                "imageUrl": b_list[i][2],
                "link": {
                    "web": b_list[i][3]
                }
            })

        res = {
          "version": "2.0",
          "template": {
            "outputs": [
              {
                  "listCard": {
                      "header": {
                          "title": answer
                      },
                      "items": j_list,
                      "buttons": [
                          {
                              "label": "더보기",
                              "action": "webLink",
                              "webLinkUrl": "https://m.boannews.com/html/news.html?mtype=1&tab_type=1#sec1"
                          }
                      ]
                  }
              }
            ],
            "quickReplies": [
              {
                "messageText": "메뉴",
                "action": "message",
                "label": "메뉴"
              }
            ]
          }
        }

    # 데일리시큐
    elif answer == "데일리시큐's 주간":
        adpath = path + '/admin/_weekly/데일리시큐'
        f = open(adpath, 'r')
        N = int(f.read())
        f = open(adpath, 'w+t')
        f.write(str(N + 1))

        d_list = week_daily()

        j_list = []
        for i in range(5):
            j_list.append({
                "title": d_list[i][0],
                "imageUrl": d_list[i][1],
                "link": {
                    "web": d_list[i][2]
                }
            })

        res = {
          "version": "2.0",
          "template": {
            "outputs": [
              {
                  "listCard": {
                      "header": {
                          "title": answer
                      },
                      "items": j_list,
                      "buttons": [
                          {
                              "label": "더보기",
                              "action": "webLink",
                              "webLinkUrl": "https://dailysecu.com/news/articleList.html?view_type=sm"
                          }
                      ]
                  }
              }
            ],
            "quickReplies": [
              {
                "messageText": "메뉴",
                "action": "message",
                "label": "메뉴"
              }
            ]
          }
        }

    # The Hacker News
    elif answer == "The Hacker News's 주간":
        adpath = path + '/admin/_weekly/The Hacker News'
        f = open(adpath, 'r')
        N = int(f.read())
        f = open(adpath, 'w+t')
        f.write(str(N + 1))
        
        h_list = week_hacker()

        j_list = []
        for i in range(5):
            j_list.append({
                "title": h_list[i][0],
                "imageUrl": h_list[i][1],
                "link": {
                    "web": h_list[i][2]
                }
            })

        res = {
          "version": "2.0",
          "template": {
            "outputs": [
              {
                  "listCard": {
                      "header": {
                          "title": answer
                      },
                      "items": j_list,
                      "buttons": [
                          {
                              "label": "더보기",
                              "action": "webLink",
                              "webLinkUrl": "https://thehackernews.com/"
                          }
                      ]
                  }
              }
            ],
            "quickReplies": [
              {
                "messageText": "메뉴",
                "action": "message",
                "label": "메뉴"
              }
            ]
          }
        }

    # WIRED
    elif answer == "Wired's 주간":
        adpath = path + '/admin/_weekly/Wired'
        f = open(adpath, 'r')
        N = int(f.read())
        f = open(adpath, 'w+t')
        f.write(str(N + 1))
        
        w_list = week_wired()

        j_list = []
        for i in range(5):
            j_list.append({
                "title": w_list[i][0],
                "description": w_list[i][1],
                "imageUrl": w_list[i][2],
                "link": {
                    "web": w_list[i][3]
                }
            })

        res = {
          "version": "2.0",
          "template": {
            "outputs": [
              {
                  "listCard": {
                      "header": {
                          "title": answer
                      },
                      "items": j_list,
                      "buttons": [
                          {
                              "label": "더보기",
                              "action": "webLink",
                              "webLinkUrl": "https://www.wired.com/most-popular/"
                          }
                      ]
                  }
              }
            ],
            "quickReplies": [
              {
                "messageText": "메뉴",
                "action": "message",
                "label": "메뉴"
              }
            ]
          }
        }
#########################################################################################################################################################


#################################################################### 검색 사이트 설정 ####################################################################
    # 보안뉴스
    elif answer == "보안뉴스로 설정":
        f = open(clipath + '/SearchN', 'w+t')
        f.write('0')
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "검색 사이트를 '보안뉴스'로 변경하였습니다\n\n검색어를 입력하시면 '보안뉴스'의 기사를 가져옵니다"
                        }
                    }
                ],
                "quickReplies": [
                  {
                    "messageText": "메뉴",
                    "action": "message",
                    "label": "메뉴"
                  }
                ]
            }
        }
    # 데일리시큐
    elif answer == "데일리시큐로 설정":
        f = open(clipath + '/SearchN', 'w+t')
        f.write('1')
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "검색 사이트를 '데일리시큐'로 변경하였습니다\n\n검색어를 입력하시면 '데일리시큐'의 기사를 가져옵니다"
                        }
                    }
                ],
                "quickReplies": [
                  {
                    "messageText": "메뉴",
                    "action": "message",
                    "label": "메뉴"
                  }
                ]
            }
        }
    # Wired
    elif answer == "Wired로 설정":
        f = open(clipath + '/SearchN', 'w+t')
        f.write('2')
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "검색 사이트를 Wired로 변경하였습니다\n\n검색어를 입력하시면 'Wired'의 기사를 가져옵니다"
                        }
                    }
                ],
                "quickReplies": [
                  {
                    "messageText": "메뉴",
                    "action": "message",
                    "label": "메뉴"
                  }
                ]
            }
        }

#########################################################################################################################################################


#################################################################### 뉴스 추천 ####################################################################
    ### 많이 찾아본 검색어를 통해 추천
    ### 그 검색어 안에서 가장 많이 이용한 뉴스 사이트 이용
    elif answer == "뉴스 추천":
        file_list = os.listdir(clipath + '/searched')
        f = open(clipath + '/user', 'r')
        user_num = f.read()
        if not file_list:    # 검색 로그 0개 (검색 한 기록 X)
            StrOut = user_num + " 님의 검색 데이터가 존재하지 않아 추천드릴 수 없습니다"
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": StrOut
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "messageText": "메뉴",
                            "action": "message",
                            "label": "메뉴"
                        }
                    ]
                }
            }
        else:
            temp_list = []
            for i, file_data in enumerate(file_list):
                f = open(clipath + '/searched/' + file_data, 'r')
                lines = f.readlines()
                temp_list.append((str(len(lines)), file_data))
            new_list = sorted(temp_list, reverse=True)        # 내림차순 정렬
            f = open(clipath + '/SearchN', 'r')
            N = f.read()
            list = get_list(int(N), new_list[0][1])
            j_list = []
            for i in range(1,len(list)):
                j_list.append({
                    "title": list[i][0],
                    "description": list[i][1],
                    "imageUrl": list[i][2],
                    "link": {
                        "web": list[i][3]
                    }
                })
            
            if len(list) == 1:
                res = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "simpleText": {
                                    "text": "검색 결과가 없는 키워드를 검색한 경우가 많은 것으로 확인되어 추천드리기 힘듭니다 😿"
                                }
                            }
                        ],
                        "quickReplies": [
                            {
                                "messageText": "메뉴",
                                "action": "message",
                                "label": "메뉴"
                            }
                        ]
                    }
                }
            else:
                res = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "simpleText": {
                                    "text": user_num + " 님의 데이터를 분석하여 뉴스를 추천해드립니다"
                                }
                            },
                            {
                                "listCard": {
                                    "header": {
                                        "title": "뉴스 추천"
                                    },
                                    "items": j_list,
                                    "buttons": [
                                        {
                                            "label": "검색 결과 더보기",
                                            "action": "webLink",
                                            "webLinkUrl": list[0]
                                        }
                                    ]
                                }
                            }
                        ],
                        "quickReplies": [
                            {
                                "messageText": "메뉴",
                                "action": "message",
                                "label": "메뉴"
                            }
                        ]
                    }
                }
#########################################################################################################################################################


#################################################################### ADMIN ####################################################################
    elif answer[:3] == "!!!":
        # 검색어 로그 조회
        if answer[3:] == "검색어":
            adpath = path + '/admin'
            file_list = os.listdir(adpath)

            # set in list (검색횟수, 검색어)
            t_list = []
            r_list = []
            for i, file_data in enumerate(file_list):
                chk = adpath + '/' + file_data
                if os.path.isfile(chk) == False:
                    continue
                f = open(adpath + '/' + file_data, 'r')
                t = len(f.readlines())
                t_list.append((t, file_data))
                r_list.append({
                    "action": "message",
                    "label": "???" + file_data,
                    "messageText": "???" + file_data,
                })

            if not t_list:
                # 데이터 x
                strOut = "검색 기록이 없습니다"
                res = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "basicCard": {
                                    "title": "사용자 검색결과 Log",
                                    "description": "이용자들의 검색어 및 횟수",
                                    "thumbnail": {
                                        "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/admin.png"
                                    }
                                }
                            },
                            {
                                "simpleText": {
                                    "text": strOut
                                }
                            }
                        ],
                        "quickReplies": [
                            {
                                "messageText": "!!!최근",
                                "action": "message",
                                "label": "!!!최근"
                            },
                            {
                                "messageText": "!!!주간",
                                "action": "message",
                                "label": "!!!주간"
                            },
                            {
                                "messageText": "!!!검색",
                                "action": "message",
                                "label": "!!!검색"
                            },
                            {
                                "messageText": "!!!검색어",
                                "action": "message",
                                "label": "!!!검색어"
                            },
                            {
                                "messageText": "!!!삭제",
                                "action": "message",
                                "label": "!!!삭제 (사용 시 주의!)"
                            },
                            {
                                "messageText": "!!!도움말",
                                "action": "message",
                                "label": "도움말"
                            },
                            {
                                "messageText": "시작",
                                "action": "message",
                                "label": "나가기"
                            }
                        ]
                    }
                }
            else:
                # sort in list
                strOut = "{:5}\t{:5}\n".format("검색횟수", "검색어")
                s_list = sorted(sorted(t_list, key = lambda x : x[1]), key = lambda x : x[0], reverse = True)
                for idx, k in enumerate(s_list):
                    # strOut += strFormat %(str(idx+1)+'.',k[1],k[0])
                    strOut += "{:10}\t\t\t\t\t\t\t{:10}\n".format(str(k[0]), k[1])

                res = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "basicCard": {
                                    "title": "사용자 검색결과 Log",
                                    "description": "이용자들의 검색어 및 횟수",
                                    "thumbnail": {
                                        "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/admin.png"
                                    }
                                }
                            },
                            {
                                "simpleText": {
                                    "text": strOut
                                }
                            }
                        ],
                        "quickReplies": r_list
                    }
                }

        # 로그 기록 삭제
        elif answer[3:] == "삭제":
            # admin path remove
            shutil.rmtree(path)

            res = {
                 "version": "2.0",
                 "template": {
                     "outputs": [
                         {
                             "basicCard": {
                                 "title": "로그 파일 삭제",
                                 "description": "전체 데이터를 삭제합니다",
                                 "thumbnail": {
                                     "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/admin.png"
                                 }
                             }
                         },
                         {
                             "simpleImage": {
                                 "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/6.PNG",
                                 "altText": "파일을 성공적으로 삭제했습니다"
                             }
                         },
                         {
                             "simpleText": {
                                 "text": "모든 Log 파일을 성공적으로 삭제 했습니다"
                             }
                         }
                     ],
                    "quickReplies": [
                        {
                            "messageText": "!!!최근",
                            "action": "message",
                            "label": "!!!최근"
                        },
                        {
                            "messageText": "!!!주간",
                            "action": "message",
                            "label": "!!!주간"
                        },
                        {
                            "messageText": "!!!검색",
                            "action": "message",
                            "label": "!!!검색"
                        },
                        {
                            "messageText": "!!!검색어",
                            "action": "message",
                            "label": "!!!검색어"
                        },
                        {
                            "messageText": "!!!삭제",
                            "action": "message",
                            "label": "!!!삭제 (사용 시 주의!)"
                        },
                        {
                            "messageText": "!!!도움말",
                            "action": "message",
                            "label": "도움말"
                        },
                        {
                            "messageText": "시작",
                            "action": "message",
                            "label": "나가기"
                        }
                    ]
                 }
            }

        # 최근뉴스 로그 조회
        elif answer[3:] == "최근":
            adpath = path + '/admin/_recent'
            file_list = os.listdir(adpath)
            t_list = []
            r_list = []

            for i, file_data in enumerate(file_list):
                chk = adpath + '/' + file_data
                if os.path.isfile(chk) == False:
                    continue
                f = open(adpath + '/' + file_data, 'r')
                t = int(f.read())
                t_list.append((t, file_data))

            strOut = "{:5}\t{:5}\n\n".format("이용횟수", "뉴스사이트")
            s_list = sorted(sorted(t_list, key = lambda x : x[1]), key = lambda x : x[0], reverse = True)
            for idx, k in enumerate(s_list):
                strOut += "{:10}\t\t\t\t\t\t\t{:10}\n".format(str(k[0]), k[1])

            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "최근 뉴스 Log",
                                "description": "'최근뉴스' Log 데이터를 불러옵니다",
                                "thumbnail": {
                                    "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/admin.png"
                                }
                            }
                        },
                        {
                            "simpleText": {
                                "text": strOut
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "messageText": "!!!최근",
                            "action": "message",
                            "label": "!!!최근"
                        },
                        {
                            "messageText": "!!!주간",
                            "action": "message",
                            "label": "!!!주간"
                        },
                        {
                            "messageText": "!!!검색",
                            "action": "message",
                            "label": "!!!검색"
                        },
                        {
                            "messageText": "!!!검색어",
                            "action": "message",
                            "label": "!!!검색어"
                        },
                        {
                            "messageText": "!!!삭제",
                            "action": "message",
                            "label": "!!!삭제 (사용 시 주의!)"
                        },
                        {
                            "messageText": "!!!도움말",
                            "action": "message",
                            "label": "도움말"
                        },
                        {
                            "messageText": "시작",
                            "action": "message",
                            "label": "나가기"
                        }
                    ]
                }
            }

        # 주간HOT뉴스 로그 조회
        elif answer[3:] == "주간": 
            adpath = path + '/admin/_weekly'
            file_list = os.listdir(adpath)
            t_list = []
            r_list = []

            for i, file_data in enumerate(file_list):
                chk = adpath + '/' + file_data
                if os.path.isfile(chk) == False:
                    continue
                f = open(adpath + '/' + file_data, 'r')
                t = int(f.read())
                t_list.append((t, file_data))

            strOut = "{:5}\t{:5}\n\n".format("이용횟수", "뉴스사이트")
            s_list = sorted(sorted(t_list, key = lambda x : x[1]), key = lambda x : x[0], reverse = True)
            for idx, k in enumerate(s_list):
                strOut += "{:10}\t\t\t\t\t\t\t{:10}\n".format(str(k[0]), k[1])

            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "주간 HOT 뉴스 사용 Log",
                                "description": "'주간 HOT 뉴스' Log 데이터를 불러옵니다",
                                "thumbnail": {
                                    "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/admin.png"
                                }
                            }
                        },
                        {
                            "simpleText": {
                                "text": strOut
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "messageText": "!!!최근",
                            "action": "message",
                            "label": "!!!최근"
                        },
                        {
                            "messageText": "!!!주간",
                            "action": "message",
                            "label": "!!!주간"
                        },
                        {
                            "messageText": "!!!검색",
                            "action": "message",
                            "label": "!!!검색"
                        },
                        {
                            "messageText": "!!!검색어",
                            "action": "message",
                            "label": "!!!검색어"
                        },
                        {
                            "messageText": "!!!삭제",
                            "action": "message",
                            "label": "!!!삭제 (사용 시 주의!)"
                        },
                        {
                            "messageText": "!!!도움말",
                            "action": "message",
                            "label": "도움말"
                        },
                        {
                            "messageText": "시작",
                            "action": "message",
                            "label": "나가기"
                        }
                    ]
                }
            }
        
        # user 추가 기능
        elif answer[3:5] == "!!":       # user name은 띄어서 주기
            user_name = answer[5:]
            log_list = os.listdir(path + '/Users')
            chk_flag = 0
            Upath = ""      # client directory path
            for i, log_usr in enumerate(log_list):
                sub_list = os.listdir(path + '/Users/' + log_usr)
                for j, usr in enumerate(sub_list):
                    f = open(path + '/Users/' + log_usr + '/' + usr + '/user', 'r')    # 유저명 read
                    nam = f.read()
                    if nam == user_name:
                        Upath = path + '/Users/' + log_usr + '/' + usr
                        chk_flag = 1
                        break
                if chk_flag == 1:
                    break

            if chk_flag == 0:
                res = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "basicCard": {
                                    "title": "기능 부여",
                                    "description": "특정 유저에게 추가 기능을 부여합니다",
                                    "thumbnail": {
                                        "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/admin.png"
                                    }
                                }
                            },
                            {
                                "simpleText": {
                                    "text": "없는 유저명입니다"
                                }
                            }
                        ],
                        "quickReplies": [
                            {
                                "messageText": "!!!최근",
                                "action": "message",
                                "label": "!!!최근"
                            },
                            {
                                "messageText": "!!!주간",
                                "action": "message",
                                "label": "!!!주간"
                            },
                            {
                                "messageText": "!!!검색",
                                "action": "message",
                                "label": "!!!검색"
                            },
                            {
                                "messageText": "!!!검색어",
                                "action": "message",
                                "label": "!!!검색어"
                            },
                            {
                                "messageText": "!!!삭제",
                                "action": "message",
                                "label": "!!!삭제 (사용 시 주의!)"
                            },
                            {
                                "messageText": "!!!도움말",
                                "action": "message",
                                "label": "도움말"
                            },
                            {
                                "messageText": "시작",
                                "action": "message",
                                "label": "나가기"
                            }
                        ]
                    }
                }
            else:
                Upath += '/AddFunc'
                f = open(Upath, 'w')
                f.write("1")
                res = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "basicCard": {
                                    "title": "기능 부여",
                                    "description": "특정 유저에게 추가 기능을 부여합니다",
                                    "thumbnail": {
                                        "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/admin.png"
                                    }
                                }
                            },
                            {
                                "simpleText": {
                                    "text": user_name + "님에게 추가 기능을 드렸습니다"
                                }
                            }
                        ],
                        "quickReplies": [
                            {
                                "messageText": "!!!최근",
                                "action": "message",
                                "label": "!!!최근"
                            },
                            {
                                "messageText": "!!!주간",
                                "action": "message",
                                "label": "!!!주간"
                            },
                            {
                                "messageText": "!!!검색",
                                "action": "message",
                                "label": "!!!검색"
                            },
                            {
                                "messageText": "!!!검색어",
                                "action": "message",
                                "label": "!!!검색어"
                            },
                            {
                                "messageText": "!!!삭제",
                                "action": "message",
                                "label": "!!!삭제 (사용 시 주의!)"
                            },
                            {
                                "messageText": "!!!도움말",
                                "action": "message",
                                "label": "도움말"
                            },
                            {
                                "messageText": "시작",
                                "action": "message",
                                "label": "나가기"
                            }
                        ]
                    }
                }

        # 검색어 찾기
        elif answer[3:] == "검색":
            adpath = path + '/admin/_Search'
            file_list = os.listdir(adpath)
            t_list = []
            r_list = []

            for i, file_data in enumerate(file_list):
                chk = adpath + '/' + file_data
                if os.path.isfile(chk) == False:
                    continue
                f = open(adpath + '/' + file_data, 'r')
                t = int(f.read())
                t_list.append((t, file_data))

            strOut = "{:5}\t{:5}\n\n".format("검색이용", "뉴스사이트")
            s_list = sorted(sorted(t_list, key = lambda x : x[1]), key = lambda x : x[0], reverse = True)
            for idx, k in enumerate(s_list):
                strOut += "{:10}\t\t\t\t\t\t\t{:10}\n".format(str(k[0]), k[1])

            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "뉴스 검색 사용 Log",
                                "description": "'뉴스 검색' Log 데이터를 불러옵니다",
                                "thumbnail": {
                                    "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/admin.png"
                                }
                            }
                        },
                        {
                            "simpleText": {
                                "text": strOut
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "messageText": "!!!최근",
                            "action": "message",
                            "label": "!!!최근"
                        },
                        {
                            "messageText": "!!!주간",
                            "action": "message",
                            "label": "!!!주간"
                        },
                        {
                            "messageText": "!!!검색",
                            "action": "message",
                            "label": "!!!검색"
                        },
                        {
                            "messageText": "!!!검색어",
                            "action": "message",
                            "label": "!!!검색어"
                        },
                        {
                            "messageText": "!!!삭제",
                            "action": "message",
                            "label": "!!!삭제 (사용 시 주의!)"
                        },
                        {
                            "messageText": "!!!도움말",
                            "action": "message",
                            "label": "도움말"
                        },
                        {
                            "messageText": "시작",
                            "action": "message",
                            "label": "나가기"
                        }
                    ]
                }
            }
        else:
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "관리자 기능 도움말",
                                "description": "관리자 기능을 알려드립니다",
                                "thumbnail": {
                                    "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/admin.png"
                                }
                            }
                        },
                        {
                            "simpleText": {
                                "text": "!!!최근 : 챗봇 사용자들의 '최근 뉴스' 사이트 LOG 목록\n\n!!!주간 : 챗봇 사용자들의 '주간 HOT 뉴스' 사이트 LOG 목록\n\n!!!검색 : 챗봇 사용자들이 사용한 '검색 사이트' LOG 목록\n\n!!!검색어 : 챗봇 사용자들의 '검색어' LOG 목록\n\n!!!삭제 : LOG 데이터 모두 삭제 ( 주의해서 사용하세요 )\n\n???( 검색어 ) : 검색어 이용시 뉴스 사이트, 검색 날짜, 검색한 유저 LOG 출력\n('!!!검색어' 에서 간편하게 이용 가능)\n\n나가기 : 관리자 모드에서 나가기\n\n!!!!!( 유저명 ) : 특정 유저에게 추가 기능 부여 (진행중)"
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "messageText": "!!!최근",
                            "action": "message",
                            "label": "!!!최근"
                        },
                        {
                            "messageText": "!!!주간",
                            "action": "message",
                            "label": "!!!주간"
                        },
                        {
                            "messageText": "!!!검색",
                            "action": "message",
                            "label": "!!!검색"
                        },
                        {
                            "messageText": "!!!검색어",
                            "action": "message",
                            "label": "!!!검색어"
                        },
                        {
                            "messageText": "!!!삭제",
                            "action": "message",
                            "label": "!!!삭제 (사용 시 주의!)"
                        },
                        {
                            "messageText": "!!!도움말",
                            "action": "message",
                            "label": "도움말"
                        },
                        {
                            "messageText": "시작",
                            "action": "message",
                            "label": "나가기"
                        }
                    ]
                }
            }
#########################################################################################################################################################


#################################################################### 단어 상세 정보 (ADMIN) ####################################################################
    elif answer[:3] == "???":
        adpath = path + '/admin'
        adpath += '/' + answer[3:]
        if os.path.isfile(adpath) == False:    # No file
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                 "title": answer[3:] + " Data Log",
                                 "description": "웹사이트, 검색 시간, 사용자 정보(해시값)",
                                 "thumbnail": {
                                     "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/admin.png"
                                 }
                             }
                        },
                        {
                            "simpleText": {
                                "text": "사용자 검색 기록이 없습니다"
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "messageText": "!!!최근",
                            "action": "message",
                            "label": "!!!최근"
                        },
                        {
                            "messageText": "!!!주간",
                            "action": "message",
                            "label": "!!!주간"
                        },
                        {
                            "messageText": "!!!검색",
                            "action": "message",
                            "label": "!!!검색"
                        },
                        {
                            "messageText": "!!!검색어",
                            "action": "message",
                            "label": "!!!검색어"
                        },
                        {
                            "messageText": "!!!삭제",
                            "action": "message",
                            "label": "!!!삭제 (사용 시 주의!)"
                        },
                        {
                            "messageText": "!!!도움말",
                            "action": "message",
                            "label": "도움말"
                        },
                        {
                            "messageText": "시작",
                            "action": "message",
                            "label": "나가기"
                        }
                    ]
                }
            }

        else:
            f = open(adpath, 'r')
            lines = f.readlines()

            # 사용자 검색
            txt = ""
            cnt = 0
            for i in lines:
                t_list = []
                at = 0        # @ idx
                end = 0        # 끝 idx

                # [사이트, 날짜 시간, 사용자]
                for j in range(len(i)):
                    if i[j] == "@":
                        at = j

                    if i[j] == ",":
                        t_list.append(i[at+2:j])
                    end += 1

                t_list.append(i[at+2:end-1])

                # 출력 (결과)
                if int(t_list[0]) == -1:
                    txt += str(cnt + 1) + '.\n' + '검색결과 X' + '\n' + t_list[1] + '\n' + t_list[2] + '\n'
                else:
                    txt += str(cnt + 1) + '.\n' + news_list[int(t_list[0])] + '\n' + t_list[1] + '\n' + t_list[2] + '\n'
                txt += '\n'
                cnt += 1

            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                 "title": "'" + answer[3:] + "'" + " Data Log",
                                 "description": "웹사이트, 검색 시간, 사용자 정보(해시값)",
                                 "thumbnail": {
                                     "imageUrl": "https://raw.githubusercontent.com/lyhyoung2/Logo/main/admin.png"
                                 }
                             }
                        },
                        {
                            "simpleText": {
                                "text": txt
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "messageText": "!!!최근",
                            "action": "message",
                            "label": "!!!최근"
                        },
                        {
                            "messageText": "!!!주간",
                            "action": "message",
                            "label": "!!!주간"
                        },
                        {
                            "messageText": "!!!검색",
                            "action": "message",
                            "label": "!!!검색"
                        },
                        {
                            "messageText": "!!!검색어",
                            "action": "message",
                            "label": "!!!검색어"
                        },
                        {
                            "messageText": "!!!삭제",
                            "action": "message",
                            "label": "!!!삭제 (사용 시 주의!)"
                        },
                        {
                            "messageText": "!!!도움말",
                            "action": "message",
                            "label": "도움말"
                        },
                        {
                            "messageText": "시작",
                            "action": "message",
                            "label": "나가기"
                        }
                    ]
                }
            }
#########################################################################################################################################################


#################################################################### 뉴스 검색 ####################################################################
    else:        # 뉴스 검색
        adpath = path + '/admin'

        ### make client ip's directory
        # ip_address = request.remote_addr    # 이것도 사용 가능
        f = open(clipath + '/SearchN', 'r')
        N = int(f.read())

        # 특수문자 감지
        special_characters = "!@#$%^&*()-+?_=,<>/'\"[]`~\\|"
        if any(c in special_characters for c in answer):
            answer = "인더포레스트"

        list = get_list(N, answer)        # 검색\

        # 답변 텍스트 설정
        if len(list) == 1 or len(list) == 0:    # 검색 결과 X
            f1 = open(clipath + '/searched/' + answer, "a")
            utcnow= datetime.datetime.utcnow()
            time_gap= datetime.timedelta(hours=9)        # 우리나라 시간 (UTC시간 기준 +9)
            now = utcnow+ time_gap
            nowDate = now.strftime('%Y-%m-%d %H:%M:%S')
            # 이용자 로그에 뉴스사이트, 검색날짜 기록
            f1.write('뉴스사이트@ ' + str(-1) + ', 검색날짜@ ' + nowDate + '\n')                    # 이용자 디렉토리 내 저장
            f = open(clipath + '/user', 'r')
            user_num = f.read()
            # 어드민 로그에 뉴스사이트, 검색날짜, 유저명(사용자키) 기록
            f2 = open(adpath + '/' + answer, "a")        # admin에 저장
            f2.write('뉴스사이트@ ' + str(-1) + ', 검색날짜@ ' + nowDate + ', 사용자@ ' + user_num + ' (' + cli + ')' + '\n')

            res = {
              "version": "2.0",
              "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "검색 결과가 없습니다."
                        }
                    }
                ],
                "quickReplies": [
                  {
                    "messageText": "메뉴",
                    "action": "message",
                    "label": "메뉴"
                  }
                ]
              }
            }

        else:       # 검색결과 찾음
            f1 = open(clipath + '/searched/' + answer, "a")
            utcnow= datetime.datetime.utcnow()
            time_gap= datetime.timedelta(hours=9)        # 우리나라 시간 (UTC시간 기준 +9)
            now = utcnow+ time_gap
            nowDate = now.strftime('%Y-%m-%d %H:%M:%S')
            # 이용자 로그에 뉴스사이트, 검색날짜 기록
            f1.write('뉴스사이트@ ' + str(N) + ', 검색날짜@ ' + nowDate + '\n')                    # 이용자 디렉토리 내 저장
            f = open(clipath + '/user', 'r')
            user_num = f.read()
            # 어드민 로그에 뉴스사이트, 검색날짜, 유저명(사용자키) 기록
            f2 = open(adpath + '/' + answer, "a")        # admin에 저장
            f2.write('뉴스사이트@ ' + str(N) + ', 검색날짜@ ' + nowDate + ', 사용자@ ' + user_num + ' (' + cli + ')' + '\n')

            # 검색 횟수 업데이트
            f2 = open(adpath + '/_Search/' + news_list[N], "r")
            rep = int(f2.read()) + 1
            f2 = open(adpath + '/_Search/' + news_list[N], "w+t")
            f2.write(str(rep))

            j_list = []
            for i in range(1,len(list)):
                j_list.append({
                    "title": list[i][0],
                    "description": list[i][1],
                    "imageUrl": list[i][2],
                    "link": {
                        "web": list[i][3]
                    }
                })

            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "listCard": {
                                "header": {
                                    "title": answer + " 검색결과"
                                },
                                "items": j_list,
                                "buttons": [
                                    {
                                        "label": "검색 결과 더보기",
                                        "action": "webLink",
                                        "webLinkUrl": list[0]
                                    }
                                ]
                            }
                        }
                    ],
                    "quickReplies": [
                      {
                        "messageText": "메뉴",
                        "action": "message",
                        "label": "메뉴"
                      }
                    ]
                }
            }

#########################################################################################################################################################
    # 답변 전송
    return jsonify(res)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, threaded=True)