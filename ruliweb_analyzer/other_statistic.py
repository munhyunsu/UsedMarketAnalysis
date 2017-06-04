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

    # 첫 timestamp
    src_file = open(src_path, 'r')
    src_csv = csv.DictReader(src_file)
    for row in itertools.islice(src_csv, 1):
        start_timestamp = row['timestamp']

    # 파일 오픈
    src_file = open(src_path, 'r')
    src_csv = csv.DictReader(src_file)

    ipset = set()
    sellerset = set()

    # 스플릿 시작
    ctimestamp = datetime.datetime.strptime(start_timestamp,
                                            '%Y.%m.%d.%H:%M')
    ctimestamp = ctimestamp - datetime.timedelta(days = 30)
    cfile = None
    ccsv = None
    ncount = 0
    ds = dict()
    ds2 = dict()
    rpro = set()
    rdis = set()
    for row in src_csv:
        if row['district'] == '안전':
            continue
        rpro.add(row['district'])
        rdis.add(row['district'] + row['city'])
        ipset.add(row['ipaddress'])
        sellerset.add(row['nickname'])
        if row['district'] != row['city']:
            ds[row['district']] = ds.get(row['district'], 0) + 1
        else:
            ds2[row['district']] = ds2.get(row['district'], 0) + 1
        #rtimestamp = row['timestamp']
        #rtimestamp = datetime.datetime.strptime(rtimestamp,
        #                                    '%Y.%m.%d.%H:%M')
        #rstr = datetime.datetime.strftime(rtimestamp,
        #                                  '%Y%m')
        #cstr = datetime.datetime.strftime(ctimestamp,
        #                                  '%Y%m')
        #nfile = False
        #while cstr != rstr:
        #    nfile = True
        #    ctimestamp = ctimestamp + datetime.timedelta(days = 30)
        #    cstr = datetime.datetime.strftime(ctimestamp,
        #                                      '%Y%m')
        #if nfile is True:
        #    print(rstr, ncount)
        #    ncount = 0
        #else:
        #    ncount = ncount + 1

    #print(rstr, ncount)
    print(len(ipset), len(sellerset))
    print(ds)
    print(ds2)
    print(rpro, rdis)
    print(len(rpro), len(rdis))
        
if __name__ == '__main__':
    sys.exit(main(sys.argv))
