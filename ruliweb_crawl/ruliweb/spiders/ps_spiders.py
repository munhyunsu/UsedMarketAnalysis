#!/usr/bin/python3

import scrapy # 스크래피
import configparser # 설정파일
import os # 출력 파일 위치
import sqlite3 # sqlite 활용
import sys # 프로그램 관리 (ex. exit)





class RuliwebSpiderPS(scrapy.Spider):
    # 스크래피용 클래스 변수
    name = 'ps' # 스파이더 이름: 이것으로 실행 호출

    # 각종 환경변수 불러오기
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('ruliweb.ini')
        # 프로그램 동작 관련
        self.debug_level = int(config['debug']['level'])
        # 로그인용 변수들
        self.id = config['login']['id']
        self.passwd = config['login']['passwd']
        # 크롤링용 변수들
        self.start_urls = config['crawl']['start_urls'].splitlines()
        self.download_delay = int(config['crawl']['download_delay'])
        self.goal = int(config['crawl']['goal'])
        self.max_page = int(config['crawl']['max_page'])
        # 출력 디렉터리 생성
        if not os.path.exists(config['file']['output_location']):
            os.makedirs(config['file']['output_location'])
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
            callback = self.url_spider)
   
    # 수집대상 게시글 URL 스파이딩
    def url_spider(self, response):
        # INFO 레벨 이하일 경우 로그인 파일 저장
        if self.debug_level <= 2:
            config = configparser.ConfigParser()
            config.read('ruliweb.ini')
            with open(config['file']['login'], 'w') as login_file:
                login_file.write(response.body.decode('utf-8'))
            print('[INFO] Login result html file saving at {0}'.format(
                  config['file']['login']))

        # 로그인 실패할 경우 수집기 종료
        if response.url != 'http://bbs.ruliweb.com':
            if self.debug_level <= 4:
                print('[ERROR] Login fail (Response URL: {0})'.format(
                      response.url))
            sys.exit(0)

        # 로그인 성공
        if self.debug_level <= 1:
            print('[DEBUG] Login success (Response URL: {0})'.format(
                  response.url))

        
