#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib
from bs4 import BeautifulSoup
import MySQLdb
import re

# 기본 문자 인코딩 방식 설정.
reload(sys)
sys.setdefaultencoding('utf-8')

def parse_html(file_url):
	# 파일 열기.
	html = open(file_url, 'r').read()
	soup = BeautifulSoup(html)

	# 게시글 번호를 가져오는 부분.
	article_number = re.split(r'[=]', soup.find_all("input", { "type": "hidden" , "id": "copyurl" })[0]["value"])[2]

	# 게시글 제목을 가져오는 부분.
	article_title = soup.find_all("font", "view_title2")[0].contents[1].encode('utf-8')

	# 게시글 작성자 닉네임을 가져오는 부분.
	try:
		article_nick = soup.find_all("img", { "border": "0", "align": "absmiddle"})[1]["alt"]
	except:
		article_nick = str(soup.find_all("font", "view_name")[0].contents[0])

	# 게시글 시간을 가져오는 부분.
	temp_time = soup.find_all("table", { "style": "table-layout:fixed" })[0]
	temp_time = re.findall(r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})", str(temp_time))
	article_time = temp_time[0][0] + '-' + temp_time[0][1] + '-' + temp_time[0][2] + ' ' + temp_time[0][3] + ':' + temp_time[0][4]

	# 게시글 가격을 가져오는 부분.
	article_prize = soup.find_all("div", "market_phone_menu02")[0].contents[0].encode('utf-8')

	# 게시글 본문을 가져오는 부분.
	tb_detail = str(soup.find_all("td", "han")[2])
	# 본문 번호를 가져오는 부분.
	# 본문 연락처
	detail_phone = re.findall(r"(\d{3})-(\d{4})-(\d{4})", tb_detail)
	if len(detail_phone) == 0:
		detail_phone = re.findall(r"(\d{3}) (\d{4}) (\d{4})", tb_detail)
	if len(detail_phone) == 0:
		detail_phone = re.findall(r"(\d{3})\.(\d{4})\.(\d{4})", tb_detail)
	if len(detail_phone) >= 1:
		detail_phone = unicode('-'.join(detail_phone[0]))
	if len(detail_phone) == 0:
		detail_phone = None

	# 본문 이메일
	detail_email = re.findall(r"(\w+)@(\w+).(\w+)", tb_detail)
	if len(detail_email) == 0:
		detail_email = re.findall(r"(\w+)@(\w+).(\w+).(\w+)", tb_detail)
	if len(detail_email) >= 1:
		if len(detail_email[0]) == 3:
			detail_email = detail_email[0][0] + '@' + detail_email[0][1] + '.' + detail_email[0][2]
		elif len(detail_email[0]) == 4:
			detail_email = detail_email[0][0] + '@' + detail_email[0][1] + '.' + detail_email[0][2] + '.' + detail_email[0][3]
		detail_email = unicode(detail_email)
	if len(detail_email) == 0:
		detail_email = None
	
	return {"article_number": article_number, "article_title": article_title, "article_nick": article_nick, "article_time": article_time, "article_prize": article_prize, "detail_phone": detail_phone, "detail_email": detail_email}

def parse_html_phone(file_url):
	try:
		html = open(file_url, 'r').read()
		article_phone = re.split(r'[\']', html)[7]
	except:
		article_phone = None

	return {"article_phone": article_phone}

# DB에 저장하는 부분
#conn = MySQLdb.connect(host="localhost", user="harny", passwd="3674", db="joonggo", charset='utf8', init_command='SET NAMES UTF8')
#x = conn.cursor()

#x.execute("""INSERT INTO nskt VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (article_number, article_time, article_title, form_id, form_nick, form_email, form_phone, form_sell, form_prize, tb_id, tb_email, tb_location, tb_sell, tb_buydate, tb_prize, tb_how, detail_kakao, detail_phone, detail_email, detail_location, detail_sell))
#conn.commit()
#conn.close()

#print title
