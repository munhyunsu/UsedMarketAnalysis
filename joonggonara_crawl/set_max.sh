#!/bin/sh

touch max_skt.txt
touch max_kt.txt
touch max_lgt.txt
touch max_fup.txt
touch max_mup.txt

find . -maxdepth 1 -type f -name 'max_*.txt' -exec sh -c "echo $1 > {}" \;
