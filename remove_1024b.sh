#!/bin/bash

here=`pwd`

cd $here/output/skt
pwd
find . -maxdepth 1 -type f -size -4096c | wc -l
find . -maxdepth 1 -type f -size -4096c -delete
cd $here/output/kt
pwd
find . -maxdepth 1 -type f -size -4096c | wc -l
find . -maxdepth 1 -type f -size -4096c -delete
cd $here/output/lgt
pwd
find . -maxdepth 1 -type f -size -4096c | wc -l
find . -maxdepth 1 -type f -size -4096c -delete
cd $here/output/fup
pwd
find . -maxdepth 1 -type f -size -4096c | wc -l
find . -maxdepth 1 -type f -size -4096c -delete
cd $here/output/mup
pwd
find . -maxdepth 1 -type f -size -4096c | wc -l
find . -maxdepth 1 -type f -size -4096c -delete
