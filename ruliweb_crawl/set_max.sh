#!/bin/sh

touch max_psp.txt
touch max_ps.txt
touch max_nds.txt
touch max_ngc.txt
touch max_xbox.txt

find . -maxdepth 1 -type f -name 'max_*.txt' -exec sh -c "echo $1 > {}" \;
