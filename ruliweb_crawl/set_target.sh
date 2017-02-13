#!/bin/sh

touch target_psp.txt
touch target_sp.txt
touch target_nds.txt
touch target_ngc.txt
touch target_xbox.txt

find . -maxdepth 1 -type f -name 'target_*.txt' -exec sh -c "echo $1 > {}" \;
