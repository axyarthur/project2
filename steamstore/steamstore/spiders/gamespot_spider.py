from scrapy import Spider, Request
from steamstore.items import GamespotItem
import re

class GamespotSpider(Spider):
	name = 'gamespot_spider'
	allowed_urls = ['https://www.gamespot.com']
	start_urls = ['https://www.gamespot.com/reviews/?review_filter_type%5Bplatform%5D=19&review_filter_type%5Bgenre%5D=55&review_filter_type%5BtimeFrame%5D=&review_filter_type%5BstartDate%5D=&review_filter_type%5BendDate%5D=&review_filter_type%5BminRating%5D=&review_filter_type%5Btheme%5D=&review_filter_type%5Bregion%5D=&review_filter_type%5Bletter%5D=&sort=date&page=1']
	
	
	def parse(self, response):
		#get number of reviews per page and total number of reviews
		reviews = response.xpath('//a[@class = "js-event-tracking"]/div/h3/text()').extract()
		num_rev = len(reviews)
		results = response.xpath('//div/ul[@class = "paginate"]/li[@class = "paginate__item paginate__results"]/text()').extract_first()
		tot_rev = list(map(lambda x: int(x), re.findall('\d+', results)))[0]
		page = tot_rev // num_rev + 1
		
		#get urls for different review pages
		result_urls = ['https://www.gamespot.com/reviews/?review_filter_type%5Bplatform%5D=19&review_filter_type%5Bgenre%5D=55&review_filter_type%5BtimeFrame%5D=&review_filter_type%5BstartDate%5D=&review_filter_type%5BendDate%5D=&review_filter_type%5BminRating%5D=&review_filter_type%5Btheme%5D=&review_filter_type%5Bregion%5D=&review_filter_type%5Bletter%5D=&sort=date&page='\
		+ str(i) for i in range(1, page + 1)]
		
		#yield each review page to next function 
		for url in result_urls[:1]:  #first page for now
			yield Request(url = url, callback = self.parse_game_page)
	
	def parse_game_page(self, response):
		#nagaviate to each game page
		game_pages = response.xpath('//article/a[@class = "js-event-tracking"]/@href').extract()
		game_urls = list(map(lambda x: "https://www.gamespot.com" + x, game_pages))
		for url in game_urls:   #first link for now
			yield Request(url = url, callback = self.game_review_page)
	
	def game_review_page(self, response):
		title = response.xpath('//div[@id = "object-stats-wrap"]//h3/a/text()').extract_first().strip()
		date = response.xpath('//dd[@class = "pod-objectStats-info__release"]/li/span/text()').extract_first()
		gs_rating = response.xpath('//div[@class = "gs-score__cell"]/span/text()').extract_first()
		user_rating = response.xpath('//dl[@class = "breakdown-reviewScores__userAvg align-vertical--child"]/dt/a/text()').extract_first()
		num_rev = response.xpath('//dl[@class = "breakdown-reviewScores__userAvg align-vertical--child"]/dd/text()').extract_first()
		num_rev = re.findall('\d+', num_rev)[0]
		developer = response.xpath('//dl[@class = "pod-objectStats-additional"]/dd[1]/a/text()').extract()
		genre = response.xpath('//dl[@class = "pod-objectStats-additional"]/dd[3]/a/text()').extract()
		
		item = GamespotItem()
		item['title'] = title
		item['developer'] = developer
		item['date'] = date
		item['genre'] = genre
		item['rating'] = gs_rating
		item['userrate'] = user_rating
		item['reviews'] = num_rev
		
		yield item
		
		
		
		
		
		
	