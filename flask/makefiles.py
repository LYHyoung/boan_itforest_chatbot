import os

def makedir_admin(path):
    os.makedirs(path + '/admin', exist_ok=True)        # admin folder

    # 검색
    tpath = path + '/admin'
    os.makedirs(tpath + '/_Search', exist_ok=True)
    ttpath = tpath + '/_Search'
    f = open(ttpath + '/보안뉴스', 'w')    # 보안뉴스에서 검색횟수
    f.write('0')
    f = open(ttpath + '/데일리시큐', 'w')    # 데일리시큐에서 검색횟수
    f.write('0')
    f = open(ttpath + '/Wired', 'w')        # Wired에서 검색횟수
    f.write('0')

    # 최근 뉴스
    os.makedirs(tpath + '/_recent', exist_ok=True)    # 최근 뉴스 이용 중 가장 많이 사용한 뉴스 사이트
    ttpath = tpath + '/_recent'
    f = open(ttpath + '/보안뉴스', 'w')
    f.write('0')
    f = open(ttpath + '/데일리시큐', 'w')
    f.write('0')
    f = open(ttpath + '/The Hacker News', 'w')
    f.write('0')
    f = open(ttpath + '/Wired', 'w')
    f.write('0')

    # 주간 HOT 뉴스
    os.makedirs(tpath + '/_weekly', exist_ok=True)    # 주간 HOT 뉴스 이용 중 가장 많이 사용한 뉴스 사이트
    ttpath = tpath + '/_weekly'
    f = open(ttpath + '/보안뉴스', 'w')
    f.write('0')
    f = open(ttpath + '/데일리시큐', 'w')
    f.write('0')
    f = open(ttpath + '/The Hacker News', 'w')
    f.write('0')
    f = open(ttpath + '/Wired', 'w')
    f.write('0')

def makedir_user(path, clipath):
    os.makedirs(clipath, exist_ok=True)
    f = open(clipath + '/SearchN', 'w')    # 검색할 뉴스사이트 설정
    f.write('0')        # 0 : 보안뉴스 (default)
    log_list = os.listdir(path + '/Users')
    f = open(clipath + '/user', 'w')
    f.write('user' + str(len(log_list)))
    os.makedirs(clipath + '/searched', exist_ok=True)        # 검색어 로깅