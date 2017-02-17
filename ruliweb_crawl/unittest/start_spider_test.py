#!/usr/bin/python3

from spiders import ruliweb_spiders

import scrapy
import unittest
from unittest import mock

class TestStartSpider(unittest.TestCase):
    # 로그인 성공/실패 확인
    def test_start_spider(self):
        mock_response = scrapy.http.Response(
                url = 'https://bbs.ruliweb.com'
            )
        spider = ruliweb_spiders.RuliwebSpider(name = 'test')
        with self.assertRaises(Exception):
            spider.start_spider(mock_response)

if __name__ == '__main__':
    unittest.main(verbosity = 2)
