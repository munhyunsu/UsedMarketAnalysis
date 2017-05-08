#!/usr/bin/env python3

import os # scandir
import sys # exit
import sqlite3 # connector
import bs4 # BeautifulSoup
import lxml

def parse_html(file_path):
    html = open(file_path, 'rb').read()
    soup = bs4.BeautifulSoup(html, 'lxml')
    # article_number
    divs = soup.find_all('div', 'cont-tab-tips')
    try:
        article_number = divs[0].contents[0][5:].strip()
    except:
        return None
    # article_phone
    spans = soup.find_all('span', 'phoneNum-type')
    try:
        article_phone = spans[0].contents[0]
        article_phone.replace(' ', '-')
        if len(article_phone) < 1:
            article_phone = None
    except:
        article_phone = None
    # return
    return {'article_number': article_number,
            'article_phone': article_phone}


def start_analyze(src_path, connector):
    """분석 시작
    """
    # 커서 생성
    cursor = connector.cursor()
    # 큐
    dir_list = list()
    dir_list.append(src_path)
    while(len(dir_list) > 0):
        dir_cursor = dir_list.pop(0)
        with os.scandir(dir_cursor) as dir_it:
            for entry in dir_it:
                if not entry.name.startswith('.') and entry.is_file():
                    ar = parse_html(entry.path)
                    if ar == None:
                        continue
                    cursor.executescript('''
                            INSERT OR IGNORE INTO ganji
                            (article_number,
                            article_phone) VALUES
                            ("''' + str(ar['article_number']) + '''", "''' +
                            str(ar['article_phone']) + '''");''')
                    connector.commit()
                else:
                    dir_list.append(entry.path)

def create_database_connector(database):
    """데이터베이스 커넥서 생성
    """
    # 데이터베이스 생성
    connector = sqlite3.connect(database)
    cursor = connector.cursor()
    # 기본 테이블 생성
    cursor.executescript('''
            CREATE TABLE IF NOT EXISTS ganji (
            article_number TEXT PRIMARY KEY NOT NULL UNIQUE,
            article_phone TEXT);
            ''')
    connector.commit()
    return connector




def main(argv):
    """인자 확인 및 분석 시작
    """
    # 인자 개수 확인
    if len(argv) < 3:
        print('Need 2 arguments')
        print('.py [SRCDIR] [OUTPUTDB]')
        return 0
    # 인자 분배
    src_path = argv[1]
    dst_path = argv[2]
    # 데이터베이스 핸들러
    connector = create_database_connector(dst_path)
    # 분석 시작
    start_analyze(src_path, connector)
    # 완료
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
