#!/bin/bash

here=`pwd`

cd $here/output/skt
pwd
find . -maxdepth 1 -type f -size -10c | wc -l
find . -maxdepth 1 -type f -size -10c -delete
cd $here/output/kt
pwd
find . -maxdepth 1 -type f -size -10c | wc -l
find . -maxdepth 1 -type f -size -10c -delete
cd $here/output/lgt
pwd
find . -maxdepth 1 -type f -size -10c | wc -l
find . -maxdepth 1 -type f -size -10c -delete
