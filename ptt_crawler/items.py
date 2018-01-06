# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PttCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    title = scrapy.Field()
#   author = scrapy.Field()
#    date = scrapy.Field()
#    content = scrapy.Field()
#    comments = scrapy.Field()
#    score = scrapy.Field()
#    url = scrapy.Field()
	title = scrapy.Field()
	modelName = scrapy.Field()
	storageSize = scrapy.Field()
	price = scrapy.Field()
	date = scrapy.Field()
	status = scrapy.Field()
