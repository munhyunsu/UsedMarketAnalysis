#!/usr/bin/python3

import os
import sys
import csv

def get_ip_region(input_path, output_path):
    # 인풋 읽을 준비
    raw_file = open(input_path, 'r')
    raw_csv = csv.DictReader(raw_file, delimiter = ',', quotechar = '"')

    # 아웃풋 준비
    region_file = open(output_path, 'w')
    region_csv = csv.DictWriter(region_file, delimiter = ',', \
            quotechar = '"', quoting = csv.QUOTE_ALL, \
            fieldnames = ['article_time', 'article_location', \
                    'article_ip'])
    region_csv.writeheader()

    # 아웃풋
    for row in raw_csv:
        region_csv.writerow({'article_time': row['article_time'], \
                'article_location': row['article_location'], \
                'article_ip': row['article_ip']})
    
    # 파일 닫기
    raw_file.close()
    region_file.close()


def main():
    if len(sys.argv) > 3:
        print('We need 2 arguments')
        print('.py [INPUTCSV] [OUTPUTCSV]')
        sys.exit()
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    get_ip_region(input_path, output_path)



if __name__ == '__main__':
    main()
