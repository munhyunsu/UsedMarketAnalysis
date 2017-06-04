#!/usr/bin/env python3

import os # makedirs
import sys # argv, exit
import csv # DictReader

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

    # 4294967295
    # 4294967294
    # 4294967292
    # ...
    count = block
    mask = 4294967295
    bi_pow = 1
    while count != 32:
        mask = mask - bi_pow
        bi_pow = bi_pow * 2
        count = count + 1

    #str_mask = str('{:032b}'.format(mask))

    #for i in range(0, 4):
    #   print str_mask[i*8:(i+1)*8]
    result_address = bi_address & mask
    result_address = '{:032b}'.format(result_address)
    #result = str(int(result_address[0:8], 2)) + '.' + str(int(result_address[8:16], 2)) + '.' + str(int(result_address[16:24], 2)) + '.' + str(int(result_address[24:36], 2)) + '/' + str(block)
    result = str(int(result_address[0:8], 2)) + '.' + str(int(result_address[8:16], 2)) + '.' + str(int(result_address[16:24], 2)) + '.' + str(int(result_address[24:36], 2))

    return result


def toprefix(src_path):
    des_path = src_path.split('/')[-1]

    src_file = open(src_path, 'r')
    src_csv = csv.DictReader(src_file)

    des_file = open('./prefixdays/' + des_path, 'w')
    des_csv = csv.DictWriter(des_file, fieldnames = [
            'articlenumber', 'timestamp',
            'ipaddress', 'ipprefix',
            'district', 'city'])
    des_csv.writeheader()

    for row in src_csv:
        crow = row.copy()
        if crow['ipaddress'] == '':
            continue
        crow['ipprefix'] = to_cidr(crow['ipaddress'], 26)
        des_csv.writerow(crow)
        

def main(argv):
    if len(argv) < 2:
        print('We need 1 arguments')
        print('.py [SRC]')
        sys.exit()
    src_path = argv[1]

    os.makedirs('./prefixdays', exist_ok = True)   

    sit = os.scandir(src_path)
    
    for entry in sit:
        if not entry.name.startswith('.') and entry.is_file():
            cip = entry.path
            toprefix(cip)
            
        
if __name__ == '__main__':
    sys.exit(main(sys.argv))
