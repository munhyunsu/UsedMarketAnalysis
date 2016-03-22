#!/usr/bin/python
# -*- coding: utf-8 -*-





##### ##### ===== 포함 파일 =====
# Database 활용
import sqlite3
# 인자 가져오기
import sys
# 디렉터리 생성
import os
# html 파싱
from bs4 import BeautifulSoup
##### ##### ===== 포함 파일 끝 =====





##### ##### ===== 함수 구현 구역 =====
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
	database_file = sys.argv[2]
	
	# 경로 내부를 보도록 확인
	if(src_path[-1] != '/'):
		src_path = src_path + '/'

	# Create Database Connector
	conn = sqlite3.connect(database_file)
	# Create Database Cursor
	cur = conn.cursor()




	category = list()
	for content in os.listdir(src_path):
		if(os.path.isfile(os.path.join(src_path, content)) is False):
			category.append(content)

	# 파일 탐색
	for subdirs in category:
		table = 'downloaded_' + subdirs
		# Create Table
		cur.execute('''
			CREATE TABLE IF NOT EXISTS ''' + table + ''' (
			article_num INTEGER PRIMARY KEY NOT NULL UNIQUE
			)'''
		)
		conn.commit()
		
		# Insert value
		subdir = src_path + subdirs + '/'
		for subfiles in os.listdir(subdir):
			try:
				article_num = int(subfiles.split('.')[0])
				cur.execute('INSERT OR IGNORE INTO ' + table + ' (article_num) VALUES (' + str(article_num) + ')'
				)
				conn.commit()
			except:
				print 'Error', subfiles
				continue

	print 'Create Complete'
##### ##### ===== 함수 구현 구역 끝 =====
	





##### ##### ===== 스크립트 구역 =====
if __name__ == '__main__':
	main()
##### ##### ===== 스크립트 구역 끝 =====
