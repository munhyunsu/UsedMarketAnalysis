#!/usr/bin/python3

import os
import sys
import csv

def count_region(input_path, output_path):
    db_file = open(input_path, 'r')
    db_csv = csv.DictReader(db_file, \
            delimiter = ',', quotechar = '"')

    count_dict = dict()
    for row in db_csv:
        region = row['region']
        count_dict[region] = count_dict.get(region, 0) + 1

    db_file.close()

    count_file = open(output_path, 'w')
    count_csv = csv.DictWriter(count_file, \
            delimiter = ',', quotechar = '"', \
            quoting = csv.QUOTE_ALL, \
            fieldnames = ['region', 'count'])
    count_csv.writeheader()

    for keys in count_dict.keys():
        count_csv.writerow(\
            {'region': keys, 'count': count_dict[keys]})

    count_file.close()



def main():
    if len(sys.argv) > 3:
        print('We need 2 output')
        print('.py [INPUTDB] [OUTPUTCSV]')
        sys.exit()

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    count_region(input_path, output_path)



if __name__ == '__main__':
    main()
