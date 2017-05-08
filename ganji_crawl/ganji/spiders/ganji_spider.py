#!/usr/bin/env python3

import scrapy # 스크래피
import logging # 로깅
import configparser # ConfigParser
import os # os.path
import sys # exit
import sqlite3 # sqlite3
import time # sleep
import random # randint
import re # re

class GanjiSpider(scrapy.Spider):
    """간지 스파이더
    간지 데이터를 수집하는 스파이더 부모 클래스
    """
    #name = None # 스파이더 이름
    name = 'ganji'

    def __init__(self, ini_file = 'ganji.ini'):
        """초기화
        """
        if self.name == None:
            print('[FATAL] setting name is needed')
            sys.exit()
        # 설정파일 저장
        self.ini_file = ini_file
        # 설정 파일 존재 확인
        if os.path.exists(ini_file) == False:
            print('[FATAL] .ini file do not exists')
            sys.exit(0)
        # 설정파일 읽어오기
        config = configparser.ConfigParser()
        config.read(self.ini_file)
        self.config = config
        # 초기화 함수 호출
        self._set_logging()
        self._prepare_output()
        self._set_crawl_policy()

        
    def _set_logging(self):
        """로그 파일 생성
        """
        # 설정 변수 불러오기
        config = self.config
        filename = config['log']['filename']
        level = config['log']['level']
        level = getattr(logging, level)
        # 로그 설정
        logging.basicConfig(filename = filename,
                            level = level,
                            format = ('%(asctime)s '
                                    + '%(levelname)s: '
                                    + '%(message)s'),
                            detefmt = '%Y.%m.%d %H:%M:%S')
        
    def _prepare_output(self):
        """출력 준비
          1. 출력 디렉터리
          2. 수집용 데이터베이스
        """
        # 설정 변수 불러오기
        config = self.config
        name = self.name
        output_dir = config['file']['output_dir']
        database = config['file']['database']
        # 출력 디렉터리 생성
        os.makedirs(output_dir, exist_ok = True)
        # 데이터베이스 연결 및 초기화
        connector = sqlite3.connect(database)
        cursor = connector.cursor()
        cursor.executescript('''
                CREATE TABLE IF NOT EXISTS list_''' +
                name + ''' (
                article_num INTEGER PRIMARY KEY NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS downloaded_''' +
                name + ''' (
                article_num INTEGER PRIMARY KEY NOT NULL UNIQUE
                );''')
        connector.commit()
        # 데이터베이스 커넥터 저장
        self.connector = connector
        self.cursor = cursor

    def _set_crawl_policy(self):
        """크롤링 준비
          - 크롤링 딜레이
          - 시작 URL
        """
        # 설정 파일 불러오기
        config = self.config
        self.start_urls = config['crawl']['start_urls'].splitlines()
        self.download_delay = int(config['crawl']['download_delay'])

    def parse(self, response):
        """URL 수집 시작
        """
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        # 설정 파일 불러오기
        config = self.config
        name = self.name
        connector = self.connector
        cursor = self.cursor
        # 내부 변수 설정
        base_url = config['crawl']['start_urls']
        article_url_form = config['crawl']['article_url_form']
        article_url_re = config['crawl']['article_url_re']
        goal = int(config['crawl']['goal'])
        max_page = int(config['crawl']['max_page'])
        page_num_re = config['crawl']['page_num_re']
        for anum in response.xpath(article_url_form).re(article_url_re):
            # 수집 대상 목록 확인
            cursor.execute('''
                    SELECT COUNT(*) FROM list_''' + name)
            list_length = int(cursor.fetchone()[0])
            # 수집 목표 달성시 제외
            if list_length >= goal:
                break
            # 이미 받은 게시글인지 확인
            cursor.execute('''
                    SELECT * FROM downloaded_''' + name +
                    ''' WHERE article_num = ''' + anum)
            if cursor.fetchone() is not None:
                logging.info('skip: {0}'.format(anum))
                continue
            # 수집 대상에 추가
            cursor.execute('''
                    INSERT OR IGNORE INTO list_''' + name +
                    ''' (article_num) VALUES (''' + anum +
                    ''')''')
            connector.commit()
        # 제한 페이지를 넘었는지 확인
        try:
            pnum = re.findall(page_num_re, response.url)
            pnum = int(pnum[0])
        except:
            pnum = 1
        # 수집 대상 목록 확인
        cursor.execute('''
                SELECT COUNT(*) FROM list_''' + name)
        list_length = int(cursor.fetchone()[0])
        # 수집 목표 달성시 제외
        if (list_length >= goal) or (pnum >= max_page):
            return self.crawl_article()
        else:
            request_url = base_url
            request_url = base_url + 'o' + str(pnum + 1) + '/'
            return scrapy.Request(url = request_url,
                    callback = self.parse)

    def crawl_article(self):
        """문서 요청
        """
        # 설정 파일 불러오기
        config = self.config
        name = self.name
        connector = self.connector
        cursor = self.cursor
        # 변수 준비
        base_url = config['crawl']['start_urls']
        # 수집 대상 리스트 불러오기
        cursor.execute('''
                SELECT * FROM list_''' + name)
        article_list = cursor.fetchall()
        # Request 보내기
        for anum in article_list:
            # int to str
            article_number = str(anum[0])
            # url 조립
            request_url = base_url + article_number + 'x.htm'
            # Request를 날리기 전 목록에서 제거
            cursor.execute('''
                    DELETE FROM list_''' + name +
                    ''' WHERE article_num = ''' + article_number)
            connector.commit()
            # 랜덤 sleep
            time.sleep(random.randint(0, 3))
            # 요청 전송
            yield scrapy.Request(url = request_url,
                                 callback = self.save_article)

    def save_article(self, response):
        """문서 저장
        """
        # 설정 파일 불러오기
        config = self.config
        name = self.name
        connector = self.connector
        cursor = self.cursor
        # 변수 준비
        article_url_re = config['crawl']['article_url_re']
        output_dir = config['file']['output_dir']
        # 응답 문서 확인
        article_number = re.findall(article_url_re, response.url)[0]
        # 수집한 게시글 파일로 저장
        save_location = output_dir + '/' + article_number + 'x.htm'
        with open(save_location, 'wb') as html_file:
            html_file.write(response.body)
        # 다운로드 DB에 저장
        cursor.execute('''
                INSERT OR IGNORE INTO downloaded_''' + name +
                ''' (article_num) VALUES (''' + article_number +
                ''')''')
        connector.commit()
