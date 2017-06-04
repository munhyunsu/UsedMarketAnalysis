#!/usr/bin/env python3

import os # makedirs
import sys # argv, exit
import csv # DictReader


def cutoffdict(cdict):
    rdict = dict()
    
    for key in cdict.keys():
        candi = cdict[key]
        top = max(candi, key = candi.get)
        if candi[top] > (sum(candi.values())*0.5):
            rdict[key] = top

    return rdict


def groupbyprefix(src_path):
    des_path = src_path.split('/')[-1]

    src_file = open(src_path, 'r')
    src_csv = csv.DictReader(src_file)

    des_file = open('./dbdays/' + des_path, 'w')
    des_csv = csv.DictWriter(des_file, fieldnames = [
            'ipprefix', 'district', 'city'])
    des_csv.writeheader()

    cdict = dict()
    for row in src_csv:
        cprefix = row['ipprefix']
        ccity = row['district'] +' ' + row['city']
        cdict[cprefix] = {ccity: cdict.get(cprefix, dict()).get(ccity, 0) + 1}

    wdict = cutoffdict(cdict)
    for prefix in wdict.keys():
        district = wdict[prefix].split(' ')[0]
        city = wdict[prefix].split(' ')[1]
        des_csv.writerow({'ipprefix': prefix,
                          'district': district,
                          'city': city})
        

def main(argv):
    if len(argv) < 2:
        print('We need 1 arguments')
        print('.py [SRC]')
        sys.exit()
    src_path = argv[1]

    os.makedirs('./dbdays', exist_ok = True)   

    sit = os.scandir(src_path)
    
    for entry in sit:
        if not entry.name.startswith('.') and entry.is_file():
            cip = entry.path
            groupbyprefix(cip)
            
        
if __name__ == '__main__':
    sys.exit(main(sys.argv))
