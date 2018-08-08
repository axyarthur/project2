from selenium import webdriver
import time
import csv
import re
import codecs

#locate driver and get webpage
driver = webdriver.Chrome(r'C:\users\axyar\Downloads\chromedriver.exe')
#driver.get("https://store.steampowered.com/tags/en/Strategy/#p=0&tab=ConcurrentUsers")   #website first scrap attemp

driver.get("https://store.steampowered.com/search/?tags=9&page=1")                               #website 2nd scrape attempt


csv_file = codecs.open('steam_review.csv', 'a', encoding = 'utf-8')   #initialize csv file
writer = csv.writer(csv_file)
index = 1   
page_num = int(driver.find_element_by_xpath('//div[@class = "search_pagination"]/div/a[last()-1]').text)   #total page number

while index <= page_num:
	print("Scrapping page: " + str(index))
	index += 1
	game_list = driver.find_elements_by_xpath('//div[@id = "search_result_container"]/div/a')
	steam_reviews = {}
	for i in range(1, len(game_list)+1):
		#get title of game
		title = driver.find_element_by_xpath('//div[@id = "search_result_container"]/div/a[' + str(i) + ']//div[@class = "col search_name ellipsis"]/span').text
		title2 = re.sub("[^\s\da-zA-Z'.%:,\-\)\(+!]", '', title)    #gets rid of unwanted characters in string, including non-English characters
		#get steam rating of game, if no rating, return empty string
		try:
			rating = driver.find_element_by_xpath('//div[@id = "search_result_container"]/div/a[' + str(i) + ']//div[@class = "col search_reviewscore responsive_secondrow"]/span').get_attribute("data-tooltip-html")
		except:
			rating = ''
		#get price of game, get original price if there's discount
		try:
			price = driver.find_element_by_xpath('//div[@id = "search_result_container"]/div/a[' + str(i) + ']//div[@class = "col search_price_discount_combined responsive_secondrow"]/div[@class = "col search_price discounted responsive_secondrow"]/span/strike').text
		except:
			price = driver.find_element_by_xpath('//div[@id="search_result_container"]/div/a[' + str(i) + ']/div[2]/div[4]/div[2]').text
		
		steam_reviews['title'] = title2
		steam_reviews['rating'] = rating
		steam_reviews['price'] = price
		try:
			writer.writerow(steam_reviews.values())
		except UnicodeEncodeError as e:
			print(e)

	# find and press next page
	next_button = driver.find_element_by_xpath('//div[@class = "search_pagination"]/div/a[last()]')   
	next_button.click()
	time.sleep(2)
csv_file.close()
driver.close()