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
	# 파일 열기.
	html = open(file_path, 'r').read()
	soup = bs4.BeautifulSoup(html)

	# 게시글 번호를 가져오는 부분.
	article_number = re.split(r'[=]', soup.find_all("input", { "type": "hidden" , "id": "copyurl" })[0]["value"])[2]
	article_number = article_number.encode('utf-8')

	# 게시글 제목을 가져오는 부분.
	article_title = soup.find_all("font", "view_title2")[0].contents[1].encode('utf-8')
	article_title = article_title.replace('"', '_')

	# 게시글 작성자 닉네임을 가져오는 부분.
	try:
		article_nick = soup.find_all("img", { "border": "0", "align": "absmiddle"})[1]["alt"]
	except:
		#article_nick = str(soup.find_all("font", "view_name")[0].contents[0])
		article_nick = soup.find_all("font", "view_name")[0].contents[0]
	article_nick = article_nick.encode('utf-8')
	article_nick = article_nick.replace('"', '_')

	# 게시글 시간을 가져오는 부분.
	temp_time = soup.find_all("table", { "style": "table-layout:fixed" })[0]
	temp_time = re.findall(r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})", str(temp_time))
	article_time = temp_time[0][0] + '.' + temp_time[0][1] + '.' + temp_time[0][2] + '. ' + temp_time[0][3] + ':' + temp_time[0][4]

	# 게시글 가격을 가져오는 부분.
	try:
		article_prize = soup.find_all("div", "market_phone_menu02")[0].contents[0].encode('utf-8')
	except:
		article_prize = None

	# 게시글 번호를 가져오는 부분.
	temp_phone = soup.find_all('div', 'market_phone_menu03')[0]
	temp_phone = temp_phone.find_all('img')
	if len(temp_phone) > 0:
		article_phone = True
	else:
		article_phone = False

	# 게시글 본문을 가져오는 부분.
	try:
		tb_detail = str(soup.find_all("td", "han")[2])
	except:
		tb_detail = str(soup.find_all('table', {'border': '0', 'cellspacing': '0', 
			'cellpadding': '0', 'width': '100%'})[1])

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
	
	return {"article_number": article_number, "article_title": article_title, "article_nick": article_nick, "article_time": article_time, "article_prize": article_prize, "article_phone": article_phone, "detail_phone": detail_phone, "detail_email": detail_email}
##### End of parse_html()




##### insert_to_db()
def insert_to_db(conn, cur, file_path):
	article_number = re.split(r'[/]', file_path)[-1]
	article_number = article_number[:-5]
	cur.execute('SELECT * FROM ppomppu WHERE article_number = ' + str(article_number)
	)
	if cur.fetchone() is not None:
		print 'Already Insert: ' + str(article_number)
	else:
		try:
			result = parse_html(file_path)
			try:
				query = 'INSERT OR IGNORE INTO ppomppu \
				(article_number, article_title, \
				article_time, article_nick, \
				article_prize, article_phone, \
				detail_phone, detail_email \
				) \
				VALUES (' + \
					'"' + str(result['article_number']) + '", ' + \
					'"' + str(result['article_title']) + '", ' + \
					'"' + str(result['article_time']) + '", ' + \
					'"' + str(result['article_nick']) + '", ' + \
					'"' + str(result['article_prize']) + '", ' + \
					'"' + str(result['article_phone']) + '", ' + \
					'"' + str(result['detail_phone']) + '", ' + \
					'"' + str(result['detail_email']) + \
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

	## Debug
	#cur.execute('DROP TABLE IF EXISTS ppomppu')
	#conn.commit()

	# Create Table
	cur.executescript('''
		CREATE TABLE IF NOT EXISTS ppomppu (
			article_number TEXT PRIMARY KEY NOT NULL UNIQUE,
			article_title TEXT,
			article_time TEXT,
			article_nick TEXT,
			article_prize TEXT,
			article_phone TEXT,
			detail_phone TEXT,
			detail_email TEXT
			);
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
