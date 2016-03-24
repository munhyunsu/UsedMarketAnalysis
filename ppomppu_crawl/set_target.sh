#!/bin/sh

touch target_skt.txt
touch target_kt.txt
touch target_lgt.txt

find . -maxdepth 1 -type f -name 'target_*.txt' -exec sh -c "echo $1 > {}" \;
