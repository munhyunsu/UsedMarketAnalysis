# -*- coding: utf-8 -*-

# Scrapy settings for ppompu project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'ppomppu'

SPIDER_MODULES = ['ppomppu.spiders']
NEWSPIDER_MODULE = 'ppomppu.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ppomppu (+http://www.yourdomain.com)'

#RETRY_ENABLED = False
#COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
	'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
}

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"

ITEM_PIPELINES = {
	'ppomppu.pipelines.PpomppuPipeline': 300,
}
