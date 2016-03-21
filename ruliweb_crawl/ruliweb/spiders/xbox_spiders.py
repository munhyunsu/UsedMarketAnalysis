#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 개인적인 아이디, 비밀번호 파일.
from personal.rconfig import LOGIN_ID, LOGIN_PW
# scrapy item 파일.
from ruliweb.items import RuliwebItem
# 로그인을 위한 FormRequest.
# 로그인 이후 크롤링을 위한 Request.
from scrapy.http import FormRequest, Request
# 게시판 페이지에서 각 게시글 url을 얻어온 후 url을 Spider에 넣어주기 위한 urljoin.
from urlparse import urljoin
# scrapy를 사용하기 위한 scrapy.
import scrapy
# response에서 ArticleNumber를 얻어내기위한 re.
import re
# file의 존재유무 체크를 위한 os.path
import os.path
# 랜덤 sleep을 위한 time, random
import time
import random
# 언어설정을 위한 sys
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

crawl_target = 0
crawl_count = 0
max_page = 0

## ----- ----- 
## 루리웹 스파이더 클래스.
## Current Ver = v1.4(150511)
## @ v1.4 흐름 @
## ----- -----
class XboxSpider(scrapy.Spider):
	name = 'xbox'
	global crawl_target
	global crawl_count
	global max_page
	# Download_delay 설정(v1-2S).
	download_delay = 3
	# 로그인을 하고 시작해야함.
	# 따라서 로그인 페이지에서 시작.
	start_urls = [
		'http://login.daum.net/accounts/loginform.do?url=http://ruliweb.daum.net'
	]

	# 파일로부터 수집할 개수를 읽어옴.
	# 이렇게 하는 것이 소스코드 수정 없이 수집양을 조절할 수 있음.
	target_file = open('target_xbox.txt', 'r')
	crawl_target = int(target_file.readline())
	target_file.close()
	max_file = open('max_xbox.txt', 'r')
	max_page = int(max_file.readline())
	max_file.close()

	# 로그인을 하는 함수.
	def parse(self, response):
		# 로그인을 수정하기 위한 부분
		# 각 폼에 맞게 id와 pw를 입력.
		# 이후의 쿠키는 scrapy가 알아서 관리해줌.
		return scrapy.FormRequest.from_response(
			response,
			formname='loginForm',
			formdata={'id': LOGIN_ID, 'pw': LOGIN_PW},
			clickdata={'nr': 0},
			callback=self.after_login,
		)

	# 로그인이후 게시판 List에서 각 게시글 URL을 얻기위한 함수.
	def after_login(self, response):
		# 로그인 디버깅 용.
		filename = 'output/login_xbox.html'
		with open(filename, 'wb') as f:
			f.write(response.body)
		f.close()
		# 혹시 로그인이 실패했을 경우.
		# 아직 이 장소로 예외처리가 된 경우가 없어서 정상 작동을 하는지 알 수 없음.
		if 'authentication failed' in response.body:
			# personal.config에 있는 id, pw를 임의의 정보로 넣어서 실험해보면 확인 가능.
			self.log('Login failed', level=log.ERROR)
			return
		else:
			# 다운로드 리스트 초기화
			list_f = open('output/list_xbox.txt', 'w')
			list_f.close()
			# 로그인 성공 후 게시판에서 각 게시글의 URL을 따옴.
			# 이땐 공지사항 URL도 같이 들어옴.
			# 3DS = market_nds VITA = market_psp PS4 = market_ps XBOX = market_xbox Wii = market_ngc
			return Request(url='http://market.ruliweb.daum.net/list.htm?table=market_xbox&find=&ftext=&ftext2=&ftext3=3&page=1', callback=self.parse_list, dont_filter=True)

	# 수집한 게시판 정보에서 공지사항을 제외한 게시글 URL을 파싱.
	def parse_list(self, response):
		# 글로벌 변수를 불러옴.
		global crawl_target
		global crawl_count
		global max_page
		# 다운로드 리스트를 작성하기 위한 파일 오픈.
		list_f = open('output/list_xbox.txt', 'ab')
		# 사용자가 작성한 게시글 파악
		for i in response.xpath('//a[contains(@href, "read.htm?table=market_xbox")]/@href').extract():
			if crawl_count >= crawl_target:
				break
			else:
				#print i
				article_num = re.split(r'[?=&]', i)[6]
				if os.path.isfile('output/xbox/' + article_num + '.html'):
					print 'target skip: ' + article_num
				else:
					article_url = 'http://market.ruliweb.daum.net/read.htm?table=market_xbox&page=&num=' + article_num + '\n'
					list_f.write(article_url)
					crawl_count = crawl_count + 1

		# 리스트 추가 후 닫기.
		list_f.close()

		# 목표 개수 만큼 리스트를 채웠는지 체크.
		page_num = int(re.split(r'[?&=]', response.url)[12])
		if ((crawl_count >= crawl_target) or (page_num >= max_page)):
			return self.crawl_article()
		else:
			# 목표 개수 미달인 경우 다음 페이지 불러오기.
			next_url = 'http://market.ruliweb.daum.net/list.htm?table=market_xbox&find=&ftext=&ftext2=&ftext3=3&page=' + str(page_num+1)
			return Request(url=next_url, callback=self.parse_list, dont_filter=True)
		
	# 게시글 수집.
	def crawl_article(self):
		read_list_f = open('output/list_xbox.txt', 'r')
		url_lists = read_list_f.readlines()
		for i in url_lists:
			sleep_var = random.randint(0, 1)
			time.sleep(sleep_var)
			# yield를 이용해야 Request를 보낼 수 있음.
			# 가장 오랜 시간이 걸린 부분이므로 수정을 할 시 백업본 생성 필수.
			# 또한 수정을 했을 경우 수정 이력도 남겨둘 것(비교를 위함).
			yield Request(i[:-1], callback=self.parse_article)
			
	# 각 게시글의 원본을 저장.
	def parse_article(self, response):
		# 게시글에서 Parsing을 하는 방법을 찾기위해 수집한 게시글을 파일로 저장.
		article_num = re.split(r'[?=&]', response.url)[6]
		filename = 'output/xbox/' + article_num + '.html'
		with open(filename, 'wb') as f:
			f.write(response.body)
		f.close()
