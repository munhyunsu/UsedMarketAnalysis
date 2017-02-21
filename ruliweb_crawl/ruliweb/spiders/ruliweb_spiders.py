#!/usr/bin/python3

import scrapy # 스크래피
import configparser # 설정파일
import os # 출력 파일 위치
import sqlite3 # sqlite 활용
import sys # 프로그램 관리 (ex. exit)
import time # 슬립
import random # 난수 생성
import re # 정규표현식



class RuliwebSpider(scrapy.Spider):
    # 스크래피용 클래스 변수
    name = None # 스파이더 이름: 이것으로 실행 호출

    # 각종 환경변수 불러오기
    def __init__(self, ini_file = 'ruliweb.ini'):
        # 환경 변수파일 이름 저장
        self.ini_file = ini_file
        # 설정파일 세션 확인
        self._check_ini(self.ini_file)
        # 설정파일 리드
        config = configparser.ConfigParser()
        config.read(self.ini_file)
        # 프로그램 동작 관련
        self.debug_level = int(config['debug']['level'])
        # 중간 디버깅: 이름 확인
        if self.name == None:
            if self.debug_level <= 4:
                print('[ERROR] Please set name of crawler ' + \
                      '(Now: {0})'.format(name))
        # 로그인용 변수들
        self.id = config['login']['id']
        self.passwd = config['login']['passwd']
        # 크롤링용 변수들
        self.start_urls = config['crawl']['start_urls'].splitlines()
        self.download_delay = int(config['crawl']['download_delay'])
        self.goal = int(config['crawl']['goal'])
        self.max_page = int(config['crawl']['max_page'])
        # 출력 디렉터리 생성
        if not os.path.exists(config['file']['output_location'] +
                             '/' + self.name):
            os.makedirs(config['file']['output_location'] +
                        '/' + self.name)
        # 데이터베이스 연결 및 초기화
        self.connector = sqlite3.connect(config['file']['database'])
        self.cursor = self.connector.cursor()
        self.cursor.executescript('''
                CREATE TABLE IF NOT EXISTS list_''' +
                self.name + ''' (
                article_num INTEGER PRIMARY KEY NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS downloaded_''' +
                self.name + ''' (
                article_num INTEGER PRIMARY KEY NOT NULL UNIQUE
                );
                ''')
        self.connector.commit()

    def _check_ini(self, ini_file):
        config = configparser.ConfigParser()
        config.read(ini_file)
        # 환경 변수파일 존재 및 내용 여부 확인
        if len(config.sections()) == 0:
            raise OSError('[SYSTEM] ini file is not exists (INI: {0})'\
                    .format(ini_file))
        # login 세션 확인
        if not 'login' in config:
            raise KeyError('[SYSTEM] login section is not exists in ini ' +
                    ' file (INI: {0})'.format(ini_file))
        if not 'id' in config['login']:
            raise KeyError('[SYSTEM] id fieid is not exists in ' +
                    ' login section of ini file (INI: {0})'.format(
                    ini_file))
        if len(config['login']['id']) == 0:
            raise AttributeError('[SYSTEM] id value may be None (INI: ' +
                    '{0})'.format(ini_file))
        if not 'passwd' in config['login']:
            raise KeyError('[SYSTEM] passwd fieid is not exists in ' +
                    ' login section of ini file (Name: {0})'.format(
                    ini_file))
        if len(config['login']['passwd']) == 0:
            raise AttributeError('[SYSTEM] passwd value may be None ' +
                    '(INI: {0})'.format(ini_file))
        # debug 세션 확인
        if not 'debug' in config:
            raise KeyError('[SYSTEM] debug section is not exists in ini ' +
                    ' file (INI: {0})'.format(ini_file))
        if not 'level' in config['debug']:
            raise KeyError('[SYSTEM] level fieid is not exists in ' +
                    ' debug section of ini file (INI: {0})'.format(
                    ini_file))
        if len(config['debug']['level']) == 0:
            raise AttributeError('[SYSTEM] level value may be None (INI: ' +
                    '{0})'.format(ini_file))
        # file 세션 확인
        if not 'file' in config:
            raise KeyError('[SYSTEM] file section is not exists in ini ' +
                    ' file (INI: {0})'.format(ini_file))
        if not 'output_location' in config['file']:
            raise KeyError('[SYSTEM] output_location fieid is ' +
                    'not exists in file section of ' +
                    'ini file (INI: {0})'.format(ini_file))
        if len(config['file']['output_location']) == 0:
            raise AttributeError('[SYSTEM] output_location value ' +
                    'may be None (INI: {0})'.format(ini_file))
        if not 'login' in config['file']:
            raise KeyError('[SYSTEM] login fieid is ' +
                    'not exists in file section of ' +
                    'ini file (INI: {0})'.format(ini_file))
        if len(config['file']['login']) == 0:
            raise AttributeError('[SYSTEM] login value ' +
                    'may be None (INI: {0})'.format(ini_file))
        if not 'database' in config['file']:
            raise KeyError('[SYSTEM] database fieid is ' +
                    'not exists in file section of ' +
                    'ini file (INI: {0})'.format(ini_file))
        if len(config['file']['database']) == 0:
            raise AttributeError('[SYSTEM] database value ' +
                    'may be None (INI: {0})'.format(ini_file))
        # crawl 세션 확인
        if not 'crawl' in config:
            raise KeyError('[SYSTEM] crawl section is not exists in ini ' +
                    ' file (INI: {0})'.format(ini_file))
        if not 'start_urls' in config['crawl']:
            raise KeyError('[SYSTEM] start_urls fieid is ' +
                    'not exists in crawl section of ' +
                    'ini file (INI: {0})'.format(ini_file))
        if len(config['crawl']['start_urls']) == 0:
            raise AttributeError('[SYSTEM] start_urls value ' +
                    'may be None (INI: {0})'.format(ini_file))
        if not 'download_delay' in config['crawl']:
            raise KeyError('[SYSTEM] download_delay fieid is ' +
                    'not exists in crawl section of ' +
                    'ini file (INI: {0})'.format(ini_file))
        if len(config['crawl']['download_delay']) == 0:
            raise AttributeError('[SYSTEM] download_delay value ' +
                    'may be None (INI: {0})'.format(ini_file))
        if not 'goal' in config['crawl']:
            raise KeyError('[SYSTEM] goal fieid is ' +
                    'not exists in crawl section of ' +
                    'ini file (INI: {0})'.format(ini_file))
        if len(config['crawl']['goal']) == 0:
            raise AttributeError('[SYSTEM] goal value ' +
                    'may be None (INI: {0})'.format(ini_file))
        if not 'max_page' in config['crawl']:
            raise KeyError('[SYSTEM] max_page fieid is ' +
                    'not exists in crawl section of ' +
                    'ini file (INI: {0})'.format(ini_file))
        if len(config['crawl']['max_page']) == 0:
            raise AttributeError('[SYSTEM] max_page value ' +
                    'may be None (INI: {0})'.format(ini_file))
        if not 'board_urls' in config['crawl']:
            raise KeyError('[SYSTEM] board_urls fieid is ' +
                    'not exists in crawl section of ' +
                    'ini file (INI: {0})'.format(ini_file))
        if len(config['crawl']['board_urls'].splitlines()) < 1:
            raise AttributeError('[SYSTEM] board_urls value ' +
                    'may be not 2 lines (INI: {0})'.format(ini_file))
        if not 'article_url_form' in config['crawl']:
            raise KeyError('[SYSTEM] article_url_form fieid is ' +
                    'not exists in crawl section of ' +
                    'ini file (INI: {0})'.format(ini_file))
        if len(config['crawl']['article_url_form'].splitlines()) < 1:
            raise AttributeError('[SYSTEM] article_url_form value ' +
                    'may be not 2 lines (INI: {0})'.format(ini_file))
        if not 'article_url_re' in config['crawl']:
            raise KeyError('[SYSTEM] article_url_re fieid is ' +
                    'not exists in crawl section of ' +
                    'ini file (INI: {0})'.format(ini_file))
        if len(config['crawl']['article_url_re'].splitlines()) < 1:
            raise AttributeError('[SYSTEM] article_url_re value ' +
                    'may be not 2 lines (INI: {0})'.format(ini_file))
        if not 'page_number_re' in config['crawl']:
            raise KeyError('[SYSTEM] page_number_re fieid is ' +
                    'not exists in crawl section of ' +
                    'ini file (INI: {0})'.format(ini_file))
        if len(config['crawl']['page_number_re'].splitlines()) < 1:
            raise AttributeError('[SYSTEM] page_number_re value ' +
                    'may be not 2 lines (INI: {0})'.format(ini_file))
        if not 'article_urls' in config['crawl']:
            raise KeyError('[SYSTEM] article_urls fieid is ' +
                    'not exists in crawl section of ' +
                    'ini file (INI: {0})'.format(ini_file))
        if len(config['crawl']['article_urls'].splitlines()) < 1:
            raise AttributeError('[SYSTEM] article_urls value ' +
                    'may be not 2 lines (INI: {0})'.format(ini_file))

    # 로그인 시도
    def parse(self, response):
        # 로그인 시도
        if self.debug_level <= 1:
            print('[DEBUG] Login attempt')
        return scrapy.FormRequest.from_response(
            response,
            formname = 'loginForm',
            formdata = {'user_id': self.id,
                        'user_pw': self.passwd},
            clickdata = {'nr': 0},
            callback = self.start_spider)

    # 수집대상 게시글 URL 스파이딩
    def start_spider(self, response):
        # INFO 레벨 이하일 경우 로그인 파일 저장
        if self.debug_level <= 2:
            config = configparser.ConfigParser()
            config.read(self.ini_file)
            with open(config['file']['login'], 'w') as login_file:
                login_file.write(response.body.decode('utf-8'))
            print('[INFO] Login result html file saving at {0}'.format(
                  config['file']['login']))

        # 로그인 실패할 경우 수집기 종료
        if response.url != 'http://bbs.ruliweb.com':
            if self.debug_level <= 4:
                print('[ERROR] Login fail (Response URL: {0})'.format(
                      response.url))
            raise Exception('[FATAL] Login fail')

        # 로그인 성공
        if self.debug_level <= 1:
            print('[DEBUG] Login success (Response URL: {0})'.format(
                  response.url))

        # 게시판 첫페이지 요청
        request_url = config['crawl']['board_urls'].splitlines()
        request_url = request_url[0] + self.name + \
                      request_url[1] + str(1)
        if self.debug_level <= 1:
            print('[DEBUG] Request page (URL: {0})'.format(
                  request_url))
        return scrapy.Request(url = request_url,
                       callback = self.url_spider) # dont_filter = True)

    # 수집한 게시판 정보에서 게시글 URL 파싱: 공지사항 제외
    def url_spider(self, response):
        config = configparser.ConfigParser()
        config.read(self.ini_file)
        article_url_form = config['crawl']['article_url_form'].splitlines()
        article_url_form = article_url_form[0] + self.name + \
                           article_url_form[1]
        article_url_re = config['crawl']['article_url_re'].splitlines()

        # 사용한 게시글
        for ahref in response.xpath(article_url_form).extract():
            # 수집 대상 URL 수 확인
            self.cursor.execute('''
                    SELECT COUNT(*) FROM list_''' + self.name)
            list_length = int(self.cursor.fetchone()[0])

            # 수집량 출력
            if self.debug_level <= 2:
                print('[INFO] Article url list length is {0}/{1}'.format(
                      list_length, self.goal))

            # 목표 수집 목표를 채웠을 경우 스파이딩 중지
            if list_length >= self.goal:
                break

            # 현제 대상 게시글 번호
            article_num = re.split(article_url_re[0],
                                   ahref)[int(article_url_re[1])]

            # 이미 받은 게시글일 경우 패스
            self.cursor.execute('''
                    SELECT  * FROM downloaded_''' + self.name +
                    ''' WHERE article_num=''' + article_num)
            if self.cursor.fetchone() is not None:
                if self.debug_level <= 1:
                    print('[DEBUG] Target skip: {0}'.format(
                          article_num))
                continue

            # 수집 대상에 추가
            self.cursor.execute('''
                    INSERT OR IGNORE INTO list_''' + self.name +
                    ''' (article_num) VALUES (''' + article_num +
                    ''')''')
            self.connector.commit()
            if self.debug_level <= 2:
                print('[INFO] Target added: {0}'.format(
                      article_num))

        # 목표 개수를 채웠는지 확인
        max_page = int(config['crawl']['max_page'])
        page_number_re = config['crawl']['page_number_re'].splitlines()
        page_number = int(re.split(page_number_re[0],
                                   response.url)[int(page_number_re[1])])
        if self.debug_level <= 2:
            print('[INFO] Spiding page is {0}/{1}'.format(
                  page_number, max_page))
        # 수집 대상 URL 수 확인
        self.cursor.execute('''
                SELECT COUNT(*) FROM list_''' + self.name)
        list_length = int(self.cursor.fetchone()[0])
        if (list_length >= self.goal) or (page_number >= max_page) or \
                (len(response.xpath(article_url_form).extract()) == 0):
            return self.crawl_article()
        else:
            # 게시판 페이지 요청
            request_url = config['crawl']['board_urls'].splitlines()
            request_url = request_url[0] + self.name + \
                          request_url[1] + str(page_number+1)
            if self.debug_level <= 1:
                print('[DEBUG] Request page (URL: {0})'.format(
                      request_url))
            return scrapy.Request(url = request_url,
                           callback = self.url_spider) #dont_filter = True)

    # 게시글 수집
    def crawl_article(self):
        # 수집 대상 리스트 불러오기
        # 참고: yield Request를 하기 때문에 cursor가 동시에 사용될 가능성이
        #       존재함. 따라서 fetchall()로 데이터를 모두 가져옴.
        #       이에 따라 메모리 사용량이 증가함.
        self.cursor.execute('''
                SELECT * FROM list_''' + self.name)
        article_list = self.cursor.fetchall()
        # url 조립 준비
        config = configparser.ConfigParser()
        config.read(self.ini_file)
        article_urls = config['crawl']['article_urls'].splitlines()

        # Request 보내기
        # 참고: 왜인지 tuple 형태로 반복
        for article_number in article_list:
            # int to str
            article_number = str(article_number[0])
            # url 조립
            request_url = article_urls[0] + self.name + \
                          article_urls[1] + article_number

            # Request를 날리기 전 목록에서 제거
            self.cursor.execute('''
                    DELETE FROM list_''' + self.name +
                    ''' WHERE article_num=''' + article_number)
            self.connector.commit()

            # 랜덤 sleep
            time.sleep(random.randint(0, 3))

            # 요청 전송
            if self.debug_level <= 1:
                print('[DEBUG] Send request (URL: {0})'.format(
                      request_url))
            yield scrapy.Request(url = request_url,
                          callback = self.save_article)

    # 게시글 저장
    def save_article(self, response):
        config = configparser.ConfigParser()
        config.read(self.ini_file)
        article_url_re = config['crawl']['article_url_re'].splitlines()

        # 응답온 게시글 다운로드 완료 DB에 저장
        article_number = re.split(article_url_re[0],
                               response.url)[int(article_url_re[1])]
        self.cursor.execute('''
                INSERT OR IGNORE INTO downloaded_''' + self.name +
                ''' (article_num) VALUES (''' + article_number +
                ''')''')
        self.connector.commit()

        # 수집한 게시글 파일로 저장
        save_location = config['file']['output_location'] + \
                        '/' + self.name + '/' + article_number + '.html'
        if self.debug_level <= 1:
            print('[DEBUG] Save file: {0}'.format(
                  save_location))
        with open(save_location, 'wb') as html_file:
            html_file.write(response.body)
