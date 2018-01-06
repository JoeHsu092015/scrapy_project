import logging
import re
from datetime import datetime

import html2text
import scrapy

from scrapy.http import FormRequest

from ptt_crawler.items import PttCrawlerItem


class PTTSpider(scrapy.Spider):
    name = 'ptt_crawler'
    allowed_domains = ['ptt.cc']
    start_urls = ('https://www.ptt.cc/bbs/mobilesales/index.html', )

    _retries = 0
    MAX_RETRY = 1

    _stop = 0
    _sampleCount = 0
    def parse(self, response):
        for href in response.css('.r-ent > div.title > a::attr(href)'):
        	if self._stop ==1:
        		break
        	url = response.urljoin(href.extract())
        	print("current count",self._sampleCount)
        	yield scrapy.Request(url, callback=self.parseArticle)

        if self._stop ==0:
            next_page = response.xpath(
                    '//div[@id="action-bar-container"]//a[contains(text(), "上頁")]/@href')
            if next_page:
            	url = response.urljoin(next_page[0].extract())
            	logging.warning('follow {}'.format(url))
            	yield scrapy.Request(url, self.parse)
            else:
            	logging.warning('no next page')
        else:
            logging.warning('data sample reached')
            

    def parseArticle(self, response):
    	sizeRex = re.compile(r'[0-9]*[gG]+',re.I)
    	modelRex = re.compile(r'[0-9X]s*',re.I)
    	priceRex = re.compile(r'欲售價格+.*[0-9]+')
    	statusRex = re.compile(r'物品狀況+.*欲售原因+')
    	priceDigitRex = re.compile(r'[0-9]+')
    	titleTmp = response.xpath(
            '//meta[@property="og:title"]/@content')[0].extract()
    	try:
    		#get SOLD article
    		if "iphone" in titleTmp.lower() and ("[販售]" in titleTmp.lower() or "賣" in titleTmp):
    			print("parse ",titleTmp)
    			storageSize = sizeRex.search(titleTmp)[0][:-1]
    			modelName = modelRex.search(titleTmp)[0].upper()
    			if "PLUS" in titleTmp.upper():
    				modelName+=(" PLUS")

    			item = PttCrawlerItem()
    			item['modelName'] = modelName
    			item['storageSize'] = storageSize
    			item['title'] = titleTmp

    			datetime_str = response.xpath(
    				'//div[@class="article-metaline"]/span[text()="時間"]/following-sibling::span[1]/text()')[
    			0].extract()
    			item['date'] = str(datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y')).split(" ")[0]

    			converter = html2text.HTML2Text()
    			converter.ignore_links = True

    			content = converter.handle(response.xpath('//div[@id="main-content"]')[ 0].extract())
    			#get price
    			priceTmp = priceRex.search(content)[0]
    			item['price'] = priceDigitRex.search(priceTmp)[0]
    			#get phone status
    			if "全新" in content :
    				item['status'] = "new"
    			else:
    				item['status'] = "old"
    			if item['date'] < "2017-12-01":
    				self._stop = 1
    			self._sampleCount += 1
    			yield item
    		else:
    			print("skip ",titleTmp)

    		pass
    	except TypeError:
    		print("Type error ")
    		raise
