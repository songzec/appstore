#-*- coding:utf-8 –*-
import scrapy
import re
import json

from scrapy.selector import Selector
from appstore.items import AppstoreItem

RENDER_HTML_URL = "http://192.168.99.100:8050/render.html"

class HuaweiSpider(scrapy.Spider):
	name = 'huawei'
	allowed_domains = ["huawei.com"]

	start_urls = [
		"http://appstore.huawei.com/more/all"
	]

	# for p in range(2, 42):
	# 	urlToCrawl = "http://appstore.huawei.com/more/all/"
	# 	urlToCrawl += str(p)
	# 	start_urls.append(urlToCrawl)

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url, self.parse, meta={
			'splash': {
					'endpoint': 'render.html',
					'args': {'wait': 0.5}
				}
			})


	def parse(self, response):
		page = Selector(response)
		print "response = " , response , "\t\n"
		print "page = " , page , "\t\n"
		hrefs = page.xpath('.//h4[@class="title"]/a/@href')

		for href in hrefs:
			url = href.extract()
			request = scrapy.Request(url, callback=self.parse_item, meta={
			'splash': {
					'endpoint': 'render.html',
					'args': {'wait': 0.5}
				}
			})
			request.meta['url'] = url
			yield request

		# find next page
		for i in range(1,10):
			nextpath = '//div[@class="page-ctrl ctrl-app"]/a[' + str(i) + ']/text()'
			if page.xpath(nextpath).extract_first().encode('utf-8') == "下一页":
				nextpage = page.xpath('//div[@class="page-ctrl ctrl-app"]/a[' + str(i) + ']/@href').extract_first()
				print nextpage
				yield scrapy.Request(nextpage, callback=self.parse, meta={
				'splash': {
						'endpoint': 'render.html',
						'args': {'wait': 0.5}
					}
				})
				break


	def parse_item(self, response):
		page = Selector(response)
		item = AppstoreItem()

		item['title'] = page.xpath('.//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()'). \
			extract_first().encode('utf-8')

		item['url'] = response.meta['url']

		item['appid'] = re.match(r'http://.*/(.*)', item['url']).group(1)

		all_intro_text = ""
		all_intro = page.xpath('.//div[@id="app_strdesc"]/text()').extract()
		for every_intro in all_intro:
			all_intro_text += every_intro.encode('utf-8')
		item['intro'] = all_intro_text

		item['icon'] = page.xpath('.//ul[@class="app-info-ul nofloat"]/li[@class="img"]/img[@class="app-ico"]/@src'). \
			extract_first()

		divs = page.xpath('//div[@class="open-info"]')
		recomm = ""
		for div in divs:
			url = div.xpath('./p[@class="name"]/a/@href').extract_first()
			recommended_appid = re.match(r'http://.*/(.*)', url).group(1)
			name = div.xpath('./p[@class="name"]/a/text()').extract_first().encode('utf-8')
			recomm += "{0}:{1},".format(recommended_appid, name)
		item['recommended'] = recomm

		yield item

	# def parse(self, response):
	# 	page = Selector(response)

	# 	divs = page.xpath('//div[@class="game-info  whole"]')
	
	# 	for div in divs:
	# 		item = AppstoreItem()
	# 		item['title'] = div.xpath('.//h4[@class="title"]/a/text()'). \
	# 			extract_first().encode('utf-8')
	# 		item['url'] = div.xpath('.//h4[@class="title"]/a/@href').extract_first()
	# 		appid = re.match(r'http://.*/(.*)', item['url']).group(1)
	# 		item['appid'] = appid
	# 		item['intro'] = div.xpath('.//p[@class="content"]/text()'). \
	# 			extract_first().encode('utf-8')
	# 		yield item