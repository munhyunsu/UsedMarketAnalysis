#!/bin/bash

python make_sqlite.py ../joonggonara_crawl/output/ joonggonara.sqlite
python make_sqlite.py ../ppomppu_crawl/output/ ppomppu.sqlite
python make_sqlite.py ../ruliweb_crawl/output/ ruliweb.sqlite
