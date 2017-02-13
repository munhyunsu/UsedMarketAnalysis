#!/bin/bash
mkdir -p ./output/ps
scrapy crawl ps
echo 'ps Done'
sleep 5

mkdir -p ./output/xbox
scrapy crawl xbox
echo 'xbox Done'
sleep 5

mkdir -p ./output/ngc
scrapy crawl ngc
echo 'ngc Done'
sleep 5

mkdir -p ./output/nds
scrapy crawl nds
echo 'nds Done'
sleep 5

mkdir -p ./output/psp
scrapy crawl psp
echo 'psp Done'
sleep 5

./remove_1024b.sh
