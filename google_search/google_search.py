#!/usr/bin/python
# -*- coding: utf-8 -*-

##### #####
# arguments
import sys
# Google API
from google import google
# csv
import csv
# sleep
import time
##### #####





##### #####

##### #####



# start main
def main():
	'''
	메인 함수
	csv 파일을 입력으로 받아 Google Search를 진행한다.
	csv 파일을 출력으로 낸다.
	'''
	# 인자 체크
	if(len(sys.argv) != 3):
		print '[ERROR] We need two arguments'
		sys.exit(0)

	print 'We get two arguments', sys.argv[1], sys.argv[2]

	# csv파일 열기
	ifile = open(sys.argv[1], 'r')
	creader = csv.reader(ifile, delimiter = ',', quotechar = '"')

	ofile = open(sys.argv[2], 'w')
	cwriter = csv.writer(ofile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)

	# csv파일 루프
	for row in creader:
		gresult = google.search(row[0], 1)
		cwriter.writerow([row[0], len(gresult)])
		time.sleep(1)

	# 파일 닫기
	ifile.close()
	ofile.close()
# end main

if __name__ == '__main__':
	main()
