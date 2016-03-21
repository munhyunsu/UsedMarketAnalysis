#!/bin/bash
mkdir -p ./output/ps
mkdir -p ./output_phone/ps
scrapy crawl ps
echo 'ps Done'
sleep 5

mkdir -p ./output/xbox
mkdir -p ./output_phone/xbox
scrapy crawl xbox
echo 'xbox Done'
sleep 5

mkdir -p ./output/ngc
mkdir -p ./output_phone/ngc
scrapy crawl ngc
echo 'ngc Done'
sleep 5

mkdir -p ./output/nds
mkdir -p ./output_phone/nds
scrapy crawl nds
echo 'nds Done'
sleep 5

mkdir -p ./output/psp
mkdir -p ./output_phone/psp
scrapy crawl psp
echo 'psp Done'
sleep 5
