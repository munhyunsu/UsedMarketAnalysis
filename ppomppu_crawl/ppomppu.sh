#!/bin/bash

mkdir -p ./output/skt
mkdir -p ./output_phone/skt
scrapy crawl skt
echo 'skt Done'
sleep 5

mkdir -p ./output/kt
mkdir -p ./output_phone/kt
scrapy crawl kt
echo 'kt Done'
sleep 5

mkdir -p ./output/lgt
mkdir -p ./output_phone/lgt
scrapy crawl lgt
echo 'lgt Done'
sleep 5

remove_1024b.sh
