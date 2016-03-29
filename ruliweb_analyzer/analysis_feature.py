#!/usr/bin/python
# -*- coding: utf-8 -*-

# 인자
import sys
# 디렉터리 리스트
import os
# 빠른 큐 활용
import collections

def main():
	if len(sys.argv) < 3:
		print 'We need 2 arguments'
		print '.py [SRC] [DES]'
		sys.exit()
	src_path = sys.argv[1]
	des_file = sys.argv[2]

	# 경로 내부를 보도록 확인
	if(src_path[-1] != '/'):
		src_path = src_path + '/'
	
	# Queue 변수
	dir_list = collections.deque() # Directory

	# Src path 추가
	dir_list.append(src_path)
	
	count = 0

	# 디렉터리 탐색
	while(len(dir_list) > 0):
		dir_cur = dir_list.popleft()
		for sub_contents in os.listdir(dir_cur):
			if(os.path.isfile(os.path.join(dir_cur, sub_contents)) is False):
				dir_list.append(dir_cur + sub_contents + '/')
			else:
				count = count + 1
				file_path = dir_cur + sub_contents
				print file_path, os.path.isfile(file_path)

	print 'Done', count



if __name__ == '__main__':
	main()
