#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import urllib.request
import json
import csv
import time



def whois_search(input_path, output_path):
    # 변수 설정
    key = ''
    query = ''
    answer = 'json'

    # 채널 디렉터리 생성
    file_dir = './whois_htmls/'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # csv read
    ipaddress_file = open(input_path, 'r')
    ipaddress_csv = csv.reader(ipaddress_file)

    # output open
    addr_file = open(output_path, 'w')
    addr_csv = csv.writer(addr_file, delimiter = ',', quotechar = '"', \
            quoting = csv.QUOTE_ALL)
    
    # ipaddress read
    for row in ipaddress_csv:
        #print(row[0])
        # json 다운로드
        print('Select', row[0])
        query = row[0]
        file_path = file_dir + query + '.json'
        whois_url = 'http://whois.kisa.or.kr/openapi/whois.jsp' + \
                '?query=' + query + \
                '&key=' + key + \
                '&answer=' + answer
        if not os.path.exists(file_path):
            print('Download', query)
            time.sleep(2)
            response = urllib.request.urlopen(whois_url)
            html = response.read()
            html_file = open(file_path, 'w')
            html_file.write(html.decode('utf-8'))
            html_file.close()
        
        # json 리드
        json_file = open(file_path, 'r')
        whois_json = json.load(json_file)

        # 주소 읽기
        if 'korean' in whois_json['whois']:
            if 'PI' in whois_json['whois']['korean']:
                addr = whois_json['whois']['korean']\
                        ['PI']['netinfo']['addr']
            elif 'ISP' in whois_json['whois']['korean']:
                addr = whois_json['whois']['korean']\
                        ['ISP']['netinfo']['addr']
        else:
            print(query, whois_json)
            addr = None

        # 주소 출력
        addr_csv.writerow([query, addr])

    # 출력 파일 닫기
    addr_file.close()

    

def main():
    # 입출력 파일 경로
    if len(sys.argv) < 2:
        print('We need 2 arguments')
        print('.py [ADDRESSCSV] [OUTPUT]')
        sys.exit()
    # 입출력 파일 경로 지정
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # 메인 메소드
    whois_search(input_path, output_path)



if __name__ == '__main__':
    main()
