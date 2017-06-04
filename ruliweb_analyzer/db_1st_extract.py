#!/usr/bin/env python3





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
# csv
import csv
# city bag
import district_bag
##### ##### ===== 추가 지역 끝=====




##### ##### ===== 함수 선언 지역 =====
##### parse_html()
def parse_html(file_path):
    # 파일 열기
    html = open(file_path, 'r').read()
    soup = bs4.BeautifulSoup(html, 'lxml')

    # 게시글 번호를 가져오는 부분.
    tds = soup.find_all("td", "con") # 제목과 동일
    articlenumber = re.split(r'[\[\]]', tds[0].b.contents[0].strip())[3]

    # 게시글 지역을 가져오는 부분.
    tds = soup.find_all("td", "con") # 제목과 동일
    district = re.split(r'[\[\]]', tds[0].b.contents[0].strip())[1]

    # 게시글 시간을 가져오는 부분.
    tables = soup.find_all("table", { "id" : "marketread" })
    temp_time = tables[0].find_all("td", { "width" : "30%" })[0].contents[0].strip()
    year = temp_time[0:4]
    month = temp_time[6:8]
    day = temp_time[10:12]
    hour = temp_time[17:19]
    minute = temp_time[21:23]
    if (temp_time[14:16] == 'PM') and (hour != '12'):
        hour = str(int(hour)+12)
    timestamp = year + '.' + month + '.' + day + '.' + hour + ':' + minute

    # 게시글 작성자 IP를 가져오는 부분.
    tables = soup.find_all("table", { "id" : "marketread" }) # 시간과 동일
    ipaddress = re.split(r'[\']', tables[0].find_all("td", { "width" : "50%" })[0].a["href"])[1]

    # 본문을 가져오는 부분.
    try:
        detail = str(tables[0].contents[9].find_all("td", "con")[0])
    except:
        print('{0} detail error'.format(articlenumber))
        detail = ''

    # 도시 검색
    city = None
    if (district != '안전') and (district != ''):
        for index_city in district_bag.district_set[district]:
            if detail.find(index_city) > 0:
                city = index_city
                break
        if city == None:
            city = district
    else:
        city = district

    return {'articlenumber': articlenumber, 
            'timestamp': timestamp,
            'ipaddress': ipaddress,
            'district': district,
            'city': city}
##### End of parse_html()




##### write_to_csv()
def write_to_csv(csv_writer, file_path, added_set):
    article_number = re.split(r'[/]', file_path)[-1]
    article_number = article_number[:-5]

#    try:
    if article_number in added_set:
        print('{0} pass'.format(article_number))
        return;
    result = parse_html(file_path)
    csv_writer.writerow(result)
    added_set.add(article_number)
#    except:
#        print('Parse Error: ' + file_path)
##### End of write_to_csv()



##### main() 시작
def main():
    if len(sys.argv) < 3:
        print('We need 2 arguments')
        print('.py [SRC] [DES]')
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
    
    # already added list
    added_set = set()
    # output file
    if os.path.exists(des_path) is True:
        with open(des_path, 'r') as output_file:
            csv_reader = csv.DictReader(output_file)
            for row in csv_reader:
                added_set.add(row['articlenumber'])
        output_file = open(des_path, 'a')
        csv_writer = csv.DictWriter(output_file, fieldnames = [
                'articlenumber', 'timestamp', 
                'ipaddress', 'district', 
                'city'])
    else:
        output_file = open(des_path, 'w')
        csv_writer = csv.DictWriter(output_file, fieldnames = [
                'articlenumber', 'timestamp', 
                'ipaddress', 'district', 
                'city'])
        csv_writer.writeheader()

    # 디렉터리 탐색
    while(len(dir_list) > 0):
        dir_cur = dir_list.popleft()
        for sub_contents in os.listdir(dir_cur):
            if(os.path.isfile(os.path.join(dir_cur, sub_contents)) is False):
                dir_list.append(dir_cur + sub_contents + '/')
            else:
                file_path = dir_cur + sub_contents
                print('{0} process'.format(file_path))
                write_to_csv(csv_writer, file_path, added_set)

    print('Done')
##### End of Main()
##### ##### ===== 함수 선언 지역 끝 =====



if __name__ == '__main__':
    main()
