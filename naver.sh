#!/bin/bash

mkdir -p ./output/skt
scrapy crawl skt
echo 'skt Done'
sleep 5

mkdir -p ./output/kt
scrapy crawl kt
echo 'kt Done'
sleep 5

mkdir -p ./output/lgt
scrapy crawl lgt
echo 'lgt Done'
sleep 5

mkdir -p ./output/fup
scrapy crawl fup
echo 'fup Done'
sleep 5

mkdir -p ./output/mup
scrapy crawl mup
echo 'mup Done'
sleep 5
