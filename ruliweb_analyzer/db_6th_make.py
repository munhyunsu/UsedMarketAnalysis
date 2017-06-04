#!/usr/bin/env python3

import os # makedirs
import sys # argv, exit
import csv # DictReader


def updatedb(ipgeo, dbdays):
    cdate = dbdays.split('/')[-1]
    cdate = cdate.split('.')[-2]
    cpersist = 0
    cnew = 0
    cupdate = 0

    dbfile = open(dbdays, 'r')
    dbcsv = csv.DictReader(dbfile)
    
    for row in dbcsv:
        if row['ipprefix'] not in ipgeo:
            ipgeo[row['ipprefix']] = {'district': row['district'],
                                      'city': row['city']}
            cnew = cnew + 1
        else:
            if (ipgeo[row['ipprefix']]['district'] == row['district']) \
                    and (ipgeo[row['ipprefix']]['city'] == row['city']):
            #if (ipgeo[row['ipprefix']]['district'] == row['district']):
                cpersist = cpersist + 1
            else:
                ipgeo[row['ipprefix']] = {'district': row['district'],
                                          'city': row['city']}
                cupdate = cupdate + 1

    return (cdate, cpersist, cnew, cupdate)

def main(argv):
    if len(argv) < 2:
        print('We need 2 arguments')
        print('.py [SRC] [DES]')
        sys.exit()
    src_path = argv[1]
    des_path = argv[2]

    sit = os.scandir(src_path)
    dbpath = list()
    for entry in sit:
        if not entry.name.startswith('.') and entry.is_file():
            dbpath.append(entry.path)
            dbpath.sort()

    des_file = open(des_path, 'w')
    des_csv = csv.DictWriter(des_file, fieldnames = [
            'date', 'persist',
            'new', 'update'])
    des_csv.writeheader()

    ipgeo = dict()
    for dbdays in dbpath:
        (cdate, cpersist, cnew, cupdate) = updatedb(ipgeo, dbdays)
        des_csv.writerow({'date': cdate,
                          'persist': cpersist,
                          'new': cnew,
                          'update': cupdate})

    tfile = open('result.csv', 'w')
    tcsv = csv.DictWriter(tfile, fieldnames = [
            'ipprefix', 'district', 'city'])
    tcsv.writeheader()
    for key in ipgeo.keys():
        tcsv.writerow({'ipprefix': key,
                       'district': ipgeo[key]['district'],
                       'city': ipgeo[key]['city']})
        
if __name__ == '__main__':
    sys.exit(main(sys.argv))
