#!/usr/bin/env python3

import sys # argv, exit
import csv # DictReader


def main(argv):
    if len(argv) < 3:
        print('We need 2 arguments')
        print('.py [SRC] [DES]')
        sys.exit()
    src_path = argv[1]
    des_path = argv[2]

    # 파일 오픈
    src_file = open(src_path, 'r')
    src_csv = csv.DictReader(src_file)

    # 정렬
    src_list = list()
    for src_row in src_csv:
        src_list.append([src_row['articlenumber'],
                        src_row['timestamp'],
                        src_row['ipaddress'],
                        src_row['district'],
                        src_row['city']])
    src_list.sort(key = lambda src_list: src_list[1])

    # 출력 파일
    des_file = open(des_path, 'w')
    des_csv = csv.DictWriter(des_file, fieldnames = [
            'articlenumber', 'timestamp',
            'ipaddress', 'district',
            'city'])
    des_csv.writeheader()
    
    for row in src_list:
        if row[1].startswith('1970'):
            continue
        if (row[3] == '안전') or (row[3] == ''):
            continue
        des_csv.writerow({'articlenumber': row[0],
                          'timestamp': row[1],
                          'ipaddress': row[2],
                          'district': row[3],
                          'city': row[4]})


if __name__ == '__main__':
    sys.exit(main(sys.argv))
