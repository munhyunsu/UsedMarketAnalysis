#!/usr/bin/python
# -*- coding: utf-8 -*-





##### ##### ===== 추가 지역 =====
# 인자
import sys
# 디렉터리 리스트
import os
# 빠른 큐 활용
import collections
# Parse HTML Documents
import bs4
# Regular Expression
import re
# Database
import sqlite3
##### ##### ===== 추가 지역 끝=====




##### ##### ===== 함수 선언 지역 =====
##### parse_html()
def parse_html(file_path):
	# 파일 열기
	html = open(file_path, 'r').read()
	soup = bs4.BeautifulSoup(html)

	# 게시글 제목을 가져오는 부분.
	tds = soup.find_all("td", "con")
	article_title = tds[0].b.contents[0].encode('utf-8').strip()
	article_title = article_title.replace('"', '_')

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
	article_time = year + '.' + month + '.' + day + '. ' + hour + ':' + minute

	# 게시글 작성자 닉네임을 가져오는 부분.
	# tables = soup.find_all("table", { "id" : "marketread" }) # 시간과 동일
	article_nick = tables[0].find_all("span")[0].contents[0].encode('utf-8').strip()
	article_nick = article_nick.replace('"', '_')

	# 게시글 작성자 IP를 가져오는 부분.
	# tables = soup.find_all("table", { "id" : "marketread" }) # 시간과 동일
	article_ip = re.split(r'[\']', tables[0].find_all("td", { "width" : "50%" })[0].a["href"])[1]

	# 게시글 가격을 가져오는 부분.
	# tables = soup.find_all("table", { "id" : "marketread" }) # 시간과 동일
	article_prize = tables[0].find_all("td", { "bgcolor" : "#ffffff" })[4].contents[0].encode('utf-8')[:-5]

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

	# 판매완료 확인
	tds = soup.find_all("td", "con")
	if(str(tds[0]).find('<strike>') != -1):
		sales_done = True
	else:
		sales_done = False

	# 이미지 수 확인
	#tds = soup.find_all("td", "con")
	if(tds[1].img is not None):
		img_count = len(tds[1].find_all('img'))
	else:
		img_count = 0

	# 본문 길이
	#tds = soup.find_all("td", "con")
	text_len = len(str(tds[1]))

	return {"article_number": article_number, "article_title": article_title, 
		"article_location": article_location, "article_time": article_time, 
		"article_nick": article_nick, "article_ip": article_ip, 
		"article_prize": article_prize, "article_phone": article_phone, 
		"detail_phone": detail_phone, "detail_email": detail_email,
		'sales_done': sales_done, 'img_count': img_count,
		'text_len': text_len}
##### End of parse_html()




##### insert_to_db()
def insert_to_db(conn, cur, file_path):
	article_number = re.split(r'[/]', file_path)[-1]
	article_number = article_number[:-5]
	cur.execute('SELECT * FROM ruliweb WHERE article_number = ' + str(article_number)
	)
	if cur.fetchone() is not None:
		print 'Already Insert: ' + str(article_number)
	else:
		try:
			result = parse_html(file_path)
			try:
				query = 'INSERT OR IGNORE INTO ruliweb \
				(article_number, article_title, \
				article_location, article_time, \
				article_nick, article_ip, \
				article_prize, article_phone, \
				detail_phone, detail_email, \
				sales_done, img_count, \
				text_len \
				) \
				VALUES (' + \
					'"' + str(result['article_number']) + '", ' + \
					'"' + str(result['article_title']) + '", ' + \
					'"' + str(result['article_location']) + '", ' + \
					'"' + str(result['article_time']) + '", ' + \
					'"' + str(result['article_nick']) + '", ' + \
					'"' + str(result['article_ip']) + '", ' + \
					'"' + str(result['article_prize']) + '", ' + \
					'"' + str(result['article_phone']) + '", ' + \
					'"' + str(result['detail_phone']) + '", ' + \
					'"' + str(result['detail_email']) + '", ' + \
					'"' + str(result['sales_done']) + '", ' + \
					'"' + str(result['img_count']) + '", ' + \
					'"' + str(result['text_len']) + \
					'")'
				cur.execute(query)
				conn.commit()
			except:
				print 'Query Error: ' + query
		except:
			print 'Parse Error: ' + file_path
##### End of insert_to_db()



##### main() 시작
def main():
	if len(sys.argv) < 3:
		print 'We need 2 arguments'
		print '.py [SRC] [DES]'
		sys.exit()
	src_path = sys.argv[1]
	des_path = sys.argv[2]

	# 경로 내부를 보도록 확인
	if(src_path[-1] != '/'):
		src_path = src_path + '/'
	
	# Queue 변수
	dir_list = collections.deque() # Directory
	# Src path 추가
	dir_list.append(src_path)
	
	# Create Database Connector
	conn = sqlite3.connect(des_path)
	# Create Database Cursor
	cur = conn.cursor()

	# Create Table
	cur.executescript('''
		CREATE TABLE IF NOT EXISTS ruliweb (
			article_number TEXT PRIMARY KEY NOT NULL UNIQUE,
			article_title TEXT,
			article_location TEXT,
			article_time TEXT,
			article_nick TEXT,
			article_ip TEXT,
			article_prize TEXT,
			article_phone TEXT,
			detail_phone TEXT,
			detail_email TEXT,
			sales_done TEXT,
			img_count TEXT,
			text_len TEXT);
		'''
	)
	conn.commit()

	# 디렉터리 탐색
	while(len(dir_list) > 0):
		dir_cur = dir_list.popleft()
		for sub_contents in os.listdir(dir_cur):
			if(os.path.isfile(os.path.join(dir_cur, sub_contents)) is False):
				dir_list.append(dir_cur + sub_contents + '/')
			else:
				file_path = dir_cur + sub_contents
				insert_to_db(conn, cur, file_path)
				#print file_path, os.path.isfile(file_path)

	print 'Done'
##### End of Main()
##### ##### ===== 함수 선언 지역 끝 =====



if __name__ == '__main__':
	main()
