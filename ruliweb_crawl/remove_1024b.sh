#!/bin/bash

here=`pwd`

cd $here/output/ps
pwd
find . -maxdepth 1 -type f -size -10c | wc -l
find . -maxdepth 1 -type f -size -10c -delete
cd $here/output/xbox
pwd
find . -maxdepth 1 -type f -size -10c | wc -l
find . -maxdepth 1 -type f -size -10c -delete
cd $here/output/ngc
pwd
find . -maxdepth 1 -type f -size -10c | wc -l
find . -maxdepth 1 -type f -size -10c -delete
cd $here/output/nds
pwd
find . -maxdepth 1 -type f -size -10c | wc -l
find . -maxdepth 1 -type f -size -10c -delete
cd $here/output/psp
pwd
find . -maxdepth 1 -type f -size -10c | wc -l
find . -maxdepth 1 -type f -size -10c -delete
