#!/usr/bin/python3

from spiders import ruliweb_spiders

import unittest
import configparser
import os
import copy

class TestInit(unittest.TestCase):
    # 매 테스트 시작전
    def setUp(self):
        config = configparser.ConfigParser()
        config['login'] = dict()
        config['login']['id'] = 'user1'
        config['login']['passwd'] = 'passwd'
        config['debug'] = dict()
        config['debug']['level'] = '0'
        config['file'] = dict()
        config['file']['output_location'] = './output'
        config['file']['login'] = './output/login.html'
        config['file']['database'] = './ruliweb.sqlite'
        config['crawl'] = dict()
        config['crawl']['start_urls'] = \
                'https://user.ruliweb.com/member/login'
        config['crawl']['download_delay'] = '3'
        config['crawl']['goal'] = '5'
        config['crawl']['max_page'] = '1'
        config['crawl']['board_urls'] = '''
                http://market.ruliweb.com/list.htm?table=market_
                &find=&ftext=&ftext2=&ftext3=&page=
            '''
        config['crawl']['article_url_form'] = '''
                //a[contains(@href, "read.htm?table=market_
                ")]/@href
            '''
        config['crawl']['article_url_re'] = '''
                [?=&]
                6
            '''
        config['crawl']['page_number_re'] = '''
                [?=&]
                12
            '''
        config['crawl']['article_urls'] = '''
                http://market.ruliweb.com/read.htm?table=market_
                &page=&num=
            '''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)

    def tearDown(self):
        if os.path.exists('test.ini'):
            os.remove('test.ini')

    # ini 파일 존재 확인: OSError 기대
    def test_ini(self):
        with self.assertRaises(OSError):
            spider = ruliweb_spiders.RuliwebSpider(ini_file = 'dumy.ini')
    # login 세션 확인: KeyError기대
    def test_login(self):
        # login
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['login'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # login-id 세션 확인: KeyError기대
    def test_login_id(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['login']['id'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # login-id 세션 확인: AttributeError
    def test_login_id_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['login']['id'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # login-passwd 세션 확인: KeyError기대
    def test_login_passwd(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['login']['passwd'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # login-passwd 세션 확인: AttributeError
    def test_login_passwd_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['login']['passwd'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')

    # debug 세션 테스트: KeyError 기대
    def test_debug(self):
        # debug
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['debug'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # debug-level 세션 확인: KeyError기대
    def test_debug_level(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['debug']['level'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # debug-level 세션 확인: AttributeError 기대
    def test_debug_level_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['debug']['level'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')

    # file 세션 테스트: KeyError 기대
    def test_file(self):
        # file
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['file'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # file-output_location 테스트: KeyError 기대
    def test_file_output_location(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['file']['output_location'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # file-output_location 테스트: AttributeError 기대
    def test_file_output_location_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['file']['output_location'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # file-login 테스트: KeyError 기대
    def test_file_login(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['file']['login'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # file-login 테스트: AttributeError 기대
    def test_file_login_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['file']['login'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # file-database 테스트: KeyError 기대
    def test_file_database(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['file']['database'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # file-database 테스트: AttributeError 기대
    def test_file_database_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['file']['database'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')

    # crawl 세션 테스트: KeyError 기대
    def test_crawl(self):
        # file
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['crawl'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-start_urls 테스트: KeyError 기대
    def test_file_start_urls(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['crawl']['start_urls'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-database 테스트: AttributeError 기대
    def test_file_start_urls_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['crawl']['start_urls'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-download_delay 테스트: KeyError 기대
    def test_file_download_delay(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['crawl']['download_delay'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-database 테스트: AttributeError 기대
    def test_file_download_delay_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['crawl']['download_delay'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-download_delay 테스트: KeyError 기대
    def test_file_download_delay(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['crawl']['download_delay'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-database 테스트: AttributeError 기대
    def test_file_download_delay_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['crawl']['download_delay'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-goal 테스트: KeyError 기대
    def test_file_goal(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['crawl']['goal'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-database 테스트: AttributeError 기대
    def test_file_goal_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['crawl']['goal'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-max_page 테스트: KeyError 기대
    def test_file_max_page(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['crawl']['max_page'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-database 테스트: AttributeError 기대
    def test_file_max_page_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['crawl']['max_page'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-board_urls 테스트: KeyError 기대
    def test_file_board_urls(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['crawl']['board_urls'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-database 테스트: AttributeError 기대
    def test_file_board_urls_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['crawl']['board_urls'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-article_url_form 테스트: KeyError 기대
    def test_file_article_url_form(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['crawl']['article_url_form'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-database 테스트: AttributeError 기대
    def test_file_article_url_form_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['crawl']['article_url_form'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-article_url_re 테스트: KeyError 기대
    def test_file_article_url_re(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['crawl']['article_url_re'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-database 테스트: AttributeError 기대
    def test_file_article_url_re_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['crawl']['article_url_re'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-page_number_re 테스트: KeyError 기대
    def test_file_page_number_re(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['crawl']['page_number_re'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-database 테스트: AttributeError 기대
    def test_file_page_number_re_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['crawl']['page_number_re'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-article_urls 테스트: KeyError 기대
    def test_file_article_urls(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        del(config['crawl']['article_urls'])
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(KeyError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')
    # crawl-database 테스트: AttributeError 기대
    def test_file_article_urls_empty(self):
        config = configparser.ConfigParser()
        config.read('test.ini')
        config['crawl']['article_urls'] = ''
        with open('test.ini', 'w') as config_file:
            config.write(config_file)
        with self.assertRaises(AttributeError):
            spider = ruliweb_spiders.RuliwebSpider(name = 'test',
                    ini_file = 'test.ini')


if __name__ == '__main__':
    unittest.main(verbosity = 2)
