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
	# 게시글 제목을 가져오는 부분.
	tds = soup.find_all("td", "con")
	article_title = tds[0].b.contents[0].encode('utf-8').strip()

	# 게시글 번호를 가져오는 부분.
	# tds = soup.find_all("td", "con") # 제목과 동일
	article_number = re.split(r'[\[\]]', tds[0].b.contents[0].encode('utf-8').strip())[3]

	# 게시글 지역을 가져오는 부분.
	# tds = soup.find_all("td", "con") # 제목과 동일
	article_location = re.split(r'[\[\]]', tds[0].b.contents[0].encode('utf-8').strip())[1]

	# 게시글 시간을 가져오는 부분.
	tables = soup.find_all("table", { "id" : "marketread" })
	temp_time = tables[0].find_all("td", { "width" : "30%" })[0].contents[0].encode('utf-8').strip()
	year = temp_time[0:4]
	month = temp_time[8:10]
	day = temp_time[14:16]
	hour = temp_time[23:25]
	minute = temp_time[29:31]
	if (temp_time[20:22] == 'PM') and (hour != '12'):
		hour = str(int(hour)+12)
	article_time = year + '-' + month + '-' + day + ' ' + hour + ':' + minute

	# 게시글 작성자 닉네임을 가져오는 부분.
	# tables = soup.find_all("table", { "id" : "marketread" }) # 시간과 동일
	article_nick = tables[0].find_all("span")[0].contents[0].strip()

	# 게시글 작성자 IP를 가져오는 부분.
	# tables = soup.find_all("table", { "id" : "marketread" }) # 시간과 동일
	article_ip = re.split(r'[\']', tables[0].find_all("td", { "width" : "50%" })[0].a["href"])[1]

	# 게시글 가격을 가져오는 부분.
	# tables = soup.find_all("table", { "id" : "marketread" }) # 시간과 동일
	article_prize = tables[0].find_all("td", { "bgcolor" : "#ffffff" })[4].contents[0][:-2]

	# 게시글 전화 번호를 가져오는 부분.
	article_phone = str(tables[0].find_all("td", { "bgcolor" : "#ffffff" })[3]).find("####")
	if article_phone == -1:
		article_phone = False
	else:
		article_phone = True
		
	# 본문을 가져오는 부분.
	tb_detail = str(tables[0].contents[9].find_all("td", "con")[0])

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

	return {"article_number": article_number, "article_title": article_title, "article_location": article_location, "article_time": article_time, "article_nick": article_nick, "article_ip": article_ip, "article_prize": article_prize, "article_phone": article_phone, "detail_phone": detail_phone, "detail_email": detail_email}

# DB에 저장하는 부분
#conn = MySQLdb.connect(host="localhost", user="harny", passwd="3674", db="joonggo", charset='utf8', init_command='SET NAMES UTF8')
#x = conn.cursor()

#x.execute("""INSERT INTO nskt VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (article_number, article_time, article_title, form_id, form_nick, form_email, form_phone, form_sell, form_prize, tb_id, tb_email, tb_location, tb_sell, tb_buydate, tb_prize, tb_how, detail_kakao, detail_phone, detail_email, detail_location, detail_sell))
#conn.commit()
#conn.close()

#print title
