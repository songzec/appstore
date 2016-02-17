# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AppstorePipeline(object):
	def __init__(self):
		self.file = open('appstore.dat', 'wb') 

	def process_item(self, item, spider):
	    val = "{:<10}\t{:<10}\t{}\t{}\r\n{}\r\n{}\r\n\r\n".format(item['appid'], item['title'], \
	    	item['intro'], item['url'], item['icon'], item['recommended'])
	    self.file.write(val)
	    return item
