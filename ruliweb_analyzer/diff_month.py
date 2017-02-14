#!/usr/bin/python3

import os
import sys
import csv


# Convert ip to CIDR
def to_cidr(ip_address, block):
    """
    Convert IP Address to CIDR string
    """
    list_address = ip_address.split('.')
    
    bi_address = list()
    for address in list_address:
        bi_address.append('{:08b}'.format(int(address)))    

    bi_address = ''.join(bi_address)
    bi_address = int(bi_address, 2)

    count = block
    mask = 4294967295
    bi_pow = 1
    while count != 32:
        mask = mask - bi_pow
        bi_pow = bi_pow * 2
        count = count + 1

    result_address = bi_address & mask
    result_address = '{:032b}'.format(result_address)

    result = str(int(result_address[0:8], 2)) + '.' + str(int(result_address[8:16], 2)) + '.' + str(int(result_address[16:24], 2)) + '.' + str(int(result_address[24:36], 2))

    return result
# End of to_cidr()



def diff_month(output_path):
    input_list = ['1501', '1502', '1503', '1504', '1505', '1506', \
            '1507', '1508', '1509', '1510', '1511', '1512', \
            '1601', '1602', '1603', '1604']

    diff_file = open(output_path, 'w')
    diff_csv = csv.DictWriter(diff_file, delimiter = ',', \
            quotechar = '"', quoting = csv.QUOTE_ALL, \
            fieldnames = ['date', 'count_new', 'count_update', 'prefix'])
    diff_csv.writeheader()

    real_db = dict()
    month_db = dict()
    for date in input_list:
        db_path = 'db' + date + '.csv'
        db_file = open(db_path, 'r')
        db_csv = csv.DictReader(db_file, \
                delimiter = ',', quotechar = '"')

        # db 읽기
        for row in db_csv:
            month_db[row['ipblock']] = row['region']

        
        count_update = 0
        count_new = 0
        for keys in month_db.keys():
            if keys in real_db.keys():
                if month_db[keys] != real_db[keys]:
                    print(real_db[keys], '->', month_db[keys])
                    real_db[keys] = month_db[keys]
                    count_update = count_update + 1
            else:
                real_db[keys] = month_db[keys]
                count_new = count_new + 1
    
        diff_csv.writerow({'date': date, \
                'count_new': count_new, \
                'count_update': count_update, \
                'prefix': len(real_db)})

        db_file.close()
    
    diff_file.close()

    diff_db_file = open('diff_db.csv', 'w')
    diff_db_csv = csv.DictWriter(diff_db_file, delimiter = ',', \
            quotechar = '"', quoting = csv.QUOTE_ALL, \
            fieldnames = ['prefix', 'region'])
    diff_db_csv.writeheader()

    for keys in real_db.keys():
        diff_db_csv.writerow({'prefix': keys, \
                'region': real_db[keys]})
    diff_db_file.close()

def main():
    if len(sys.argv) > 2:
        print('We need 1 arguments')
        print('.py [OUTPUTCSV]')
        sys.exit()
    output_path = sys.argv[1]

    diff_month(output_path)



if __name__ == '__main__':
    main()
