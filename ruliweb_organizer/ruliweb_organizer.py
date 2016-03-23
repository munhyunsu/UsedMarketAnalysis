#!/usr/bin/python
# -*- coding: utf-8 -*-





##### ##### ===== 포함 파일 =====
# 인자 가져오기
import sys
# 디렉터리 생성
import os
# 파일 옮기기
import shutil
# html 파싱
from bs4 import BeautifulSoup
# resular expression
import re
##### ##### ===== 포함 파일 끝 =====





##### ##### ===== 함수 구현 구역 =====
# 날짜를 반환하는 함수
def getDate(file_path):
	html = open(file_path, 'r').read()
	soup = BeautifulSoup(html)

	# 게시글 시간
	try:
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
	except:
		article_time = None

	return article_time



# 메인 함수
def main():
	# 인자 개수 확인
	# 1번: 출발지
	# 2번: 목적지
	if len(sys.argv) < 2:
		print 'We need 2 arguments'
		print '.py [SRC] [DES]'
		sys.exit()
	src_path = sys.argv[1]
	des_path = sys.argv[2]
	
	# 경로 내부를 보도록 확인
	if(src_path[-1] != '/'):
		src_path = src_path + '/'
	if(des_path[-1] != '/'):
		des_path = des_path + '/'

	category = list()
	for content in os.listdir(src_path):
		if(os.path.isfile(os.path.join(src_path, content)) is False):
			category.append(content)

	# 파일 탐색
	for subdirs in category:
		subdir = src_path + subdirs + '/'
		for subfiles in os.listdir(subdir):
			# 년/월/일 가져오기
			subfile = subdir + subfiles
			date = getDate(subfile)
			if date if None:
				print 'Error None Return', subdirs, subfiles
				continue
			date = date.split('.')
			year = date[0]
			month = date[1]
			day = date[2]
			path = des_path + year + '/' + month + '/' + day + '/'

			if not os.path.exists(path):
				try:
					os.makedirs(path, 0755)
				except:
					pass
			
			shutil.move(subfile, path)
			#shutil.copy(subfile, path) # for test
			#print 'Move Complete', path # for test

	# 완료 메시지
	print 'Organize Complete'
##### ##### ===== 함수 구현 구역 끝 =====
	





##### ##### ===== 스크립트 구역 =====
if __name__ == '__main__':
	main()
##### ##### ===== 스크립트 구역 끝 =====
