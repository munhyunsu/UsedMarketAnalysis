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



def prefix_per_time(input_path, output_path):
    # 인풋 읽을 준비
    raw_file = open(input_path, 'r')
    raw_csv = csv.DictReader(raw_file, delimiter = ',', quotechar = '"')

    # 아웃풋 준비
    prefix_file = open(output_path, 'w')
    prefix_csv = csv.DictWriter(prefix_file, delimiter = ',', \
            quotechar = '"', quoting = csv.QUOTE_ALL, \
            fieldnames = ['article_time', 'prefix_len'])
    prefix_csv.writeheader()

    ipblock = dict()
    ipprefix = set()
    # 아웃풋
    for row in raw_csv:
        row_address = row['article_ip']
        row_prefix = to_cidr(row_address, 26)
        ipblock[row_prefix] = ipblock.get(row_prefix, 0) + 1
        if ipblock[row_prefix] > 1:
            ipprefix.add(row_prefix)
        prefix_csv.writerow({'article_time': row['article_time'], \
                'prefix_len': len(ipprefix)})


    
    # 파일 닫기
    raw_file.close()
    prefix_file.close()


def main():
    if len(sys.argv) > 3:
        print('We need 2 arguments')
        print('.py [INPUTCSV] [OUTPUTCSV]')
        sys.exit()
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    prefix_per_time(input_path, output_path)



if __name__ == '__main__':
    main()
