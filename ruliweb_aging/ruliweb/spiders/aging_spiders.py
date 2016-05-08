#!/usr/bin/env python
# -*- coding: utf-8 -*-





##### ##### ===== 포함 파일 =====
# 개인적인 아이디, 비밀번호 파일.
from personal.rconfig import LOGIN_ID, LOGIN_PW
# scrapy item 파일.
from ruliweb.items import RuliwebItem
# 로그인을 위한 FormRequest.
# 로그인 이후 크롤링을 위한 Request.
from scrapy.http import FormRequest, Request
# scrapy를 사용하기 위한 scrapy.
import scrapy
# response에서 ArticleNumber를 얻어내기위한 re.
import re
# 랜덤 sleep을 위한 time, random
import time
import random
# BeautifulSoup
import bs4
# Csv 핸들링
import csv
##### ##### ===== 포함 파일 끝 =====





##### ##### ===== 전역 변수 지역 =====
DOWNLOAD_DELAY = 1
##### ##### ===== 전역 변수 지역 끝 =====





##### ##### ===== 프로젝트별 변수 =====
# 주요 변수
SPIDER_NAME = 'aging'
START_URL = 'http://login.daum.net/accounts/loginform.do?url=http://ruliweb.daum.net'
ARTICLE_URL = 'http://www.ppomppu.co.kr/zboard/view.php?id=market_phone&no='


# 임시 변수
AGING_IFILE = 'ppomppu_aging.csv'
AGING_OFILE = 'ppomppu_aging_output.csv'
LOGIN_FILE = 'login.html'
##### ##### ===== 프로젝트별 변수 끝 =====





##### ##### ===== 클래스 선언 지역 =====
##### ----- -----
##### 뽐뿌 스파이더 클래스
##### ----- -----
## ----- -----
class Spider(scrapy.Spider):
	name = SPIDER_NAME

	# 딜레이 설정
	download_delay = DOWNLOAD_DELAY

	# 로그인을 하고 시작해야함
	# 따라서 로그인 페이지에서 시작
	start_urls = [
		START_URL
	]

	# 로그인을 하는 함수
	def parse(self, response):
		# 로그인을 수정하기 위한 부분
		# 각 폼에 맞게 id와 pw를 입력
		# 이후의 쿠키는 scrapy가 알아서 관리해줌
		return scrapy.FormRequest.from_response(
			response,
			formname='zb_login',
			formdata={'user_id': LOGIN_ID, 'password': LOGIN_PW},
			clickdata={'nr': 0},
			callback=self.after_login
		)

	# 로그인이후 게시판 List에서 각 게시글 URL을 얻기위한 함수
	def after_login(self, response):
		# 글로벌 변수를 불러옴
		global LOGIN_FILE
		global AGING_IFILE
		global ARTICLE_URL

		# 로그인 디버깅 용
		with open(LOGIN_FILE, 'wb') as f:
			f.write(response.body)
		f.close()

		aging_ifile = open(AGING_IFILE, 'r')
		aging_reader = csv.reader(aging_ifile, delimiter = ',', quotechar = '"')

		for row in aging_reader:
			time.sleep(random.randint(0, 1))
			yield Request(url = ARTICLE_URL + str(row[0]), callback = self.parse_article)

		aging_ifile.close()


	def parse_article(self, response):
		global AGING_OFILE

		aging_ofile = open(AGING_OFILE, 'aw')
		aging_writer = csv.writer(aging_ofile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)

		exists = 'True'
		article_num = re.split(r'[?=&]', response.url)[4]

		soup = bs4.BeautifulSoup(response.body)
		divs = soup.find_all('div', 'error1')
		if(len(divs) > 0):
			exists = 'False'

		aging_writer.writerow([article_num, exists])

		aging_ofile.close()
