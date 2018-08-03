# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GamespotItem(scrapy.Item):
	# define the fields for your item here like:
	title = scrapy.Field()
	developer = scrapy.Field()
	date = scrapy.Field()
	genre = scrapy.Field()
	rating = scrapy.Field()
	userrate = scrapy.Field()
	reviews = scrapy.Field()
	
