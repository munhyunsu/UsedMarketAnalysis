#!/bin/bash
scrapy crawl ps
echo 'ps Done'
sleep 5

scrapy crawl xbox
echo 'xbox Done'
sleep 5

scrapy crawl ngc
echo 'ngc Done'
sleep 5

scrapy crawl nds
echo 'nds Done'
sleep 5

scrapy crawl psp
echo 'psp Done'
sleep 5

./remove_1024b.sh
