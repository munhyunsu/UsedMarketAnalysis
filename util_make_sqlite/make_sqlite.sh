#!/bin/bash

echo 'Joonggonara Start'
python make_sqlite.py ../joonggonara_crawl/output/ joonggonara.sqlite
echo 'Ppomppu Start'
python make_sqlite.py ../ppomppu_crawl/output/ ppomppu.sqlite
echo 'Ruliweb Start'
python make_sqlite.py ../ruliweb_crawl/output/ ruliweb.sqlite
