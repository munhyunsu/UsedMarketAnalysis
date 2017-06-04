#!/bin/bash

python3 db_2nd_sort.py db_1st.csv db_2nd.csv
python3 db_3rd_splitdata.py db_2nd.csv 
python3 db_4th_prefix.py ipdays/
python3 db_5th_group.py prefixdays/
python3 db_6th_make.py dbdays/ db_6th.csv
