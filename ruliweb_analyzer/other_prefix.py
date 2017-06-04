#!/usr/bin/env python3

import os # makedirs
import sys # argv, exit
import csv # DictReader
import itertools # islice
import datetime # datetime


def main(argv):
    if len(argv) < 2:
        print('We need 1 arguments')
        print('.py [SRC]')
        sys.exit()
    src_path = argv[1]

    # 파일 오픈
    src_file = open(src_path, 'r')
    src_csv = csv.DictReader(src_file)

    # 스플릿 시작
    ds = dict()
    ds2 = dict()
    for row in src_csv:
        if row['district'] == '안전':
            continue
        if row['district'] != row['city']:
            ds[row['district']] = ds.get(row['district'], 0) + 1
        else:
            ds2[row['district']] = ds2.get(row['district'], 0) + 1

    #print(rstr, ncount)
    print(sum(ds.values()), sum(ds2.values()))
    print(ds)
    print(ds2)
        
if __name__ == '__main__':
    sys.exit(main(sys.argv))
