from selenium import webdriver
import time
import csv
import re
import codecs

#locate driver and get webpage
driver = webdriver.Chrome(r'C:\users\axyar\Downloads\chromedriver.exe')
#driver.get("https://store.steampowered.com/tags/en/Strategy/#p=0&tab=ConcurrentUsers")   #website first scrap attemp

driver.get("https://store.steampowered.com/search/?tags=9")                               #website 2nd scrape attempt


csv_file = open('steam_review.csv', 'w', newline = '', encoding = 'utf-32')   #initialize csv file
writer = csv.writer(csv_file)
index = 1 #testing first 2 pages  
page_num = int(driver.find_element_by_xpath('//div[@class = "search_pagination"]/div/a[last()-1]').text)

while index <= page_num:
	print("Scrapping page: " + str(index))
	index += 1
	game_list = driver.find_elements_by_xpath('//div[@id = "search_result_container"]/div/a')
	steam_reviews = {}
	for i in range(1, len(game_list)+1):
		title = driver.find_element_by_xpath('//div[@id = "search_result_container"]/div/a[' + str(i) + ']//div[@class = "col search_name ellipsis"]/span').text
		title = title.replace("[^\w\d\s']", '')
		try:
			rating = driver.find_element_by_xpath('//div[@id = "search_result_container"]/div/a[' + str(i) + ']//div[@class = "col search_reviewscore responsive_secondrow"]/span').get_attribute("data-tooltip-html")
		except:
			rating = ''
		try:
			price = driver.find_element_by_xpath('//div[@id = "search_result_container"]/div/a[' + str(i) + ']//div[@class = "col search_price_discount_combined responsive_secondrow"]/div[@class = "col search_price discounted responsive_secondrow"]/span/strike').text
		except:
			price = driver.find_element_by_xpath('//div[@id="search_result_container"]/div/a[' + str(i) + ']/div[2]/div[4]/div[2]').text
			#price = driver.find_element_by_xpath('//div[@id = "search_result_container"]/div/a[' + str(i) + ']//div[@class = "col search_price_discount_combined responsive_secondrow"]/div[@class = "col search_price responsive_secondrow"]').text
		steam_reviews['title'] = title
		steam_reviews['rating'] = rating
		steam_reviews['price'] = price
		try:
			writer.writerow(steam_reviews.values())
		except UnicodeEncodeError as e:
			print(e)
		#print(steam_reviews.items())
		#title = list(map(lambda x: x.text, title_list))
		#price = list(map(lambda x: x.text, price_list))
		#origin = list(map(lambda x: x.text, origin_price_list))


#dictionary for items to get
		#steam_reviews = zip(title, price)
		#print(index)
		#for review in steam_reviews:
		#	try:
		#		writer.writerow(review)
		#	except Exception as e:
		#		codecs.replace_errors(e)
		#		print(e)
				
#steam_reviews['date'] = date
#steam_reviews['developer'] = developer
#steam_reviews['user_rate'] = user_rate
#steam_reviews['reviews'] = reviews
	next_button = driver.find_element_by_xpath('//div[@class = "search_pagination"]/div/a[last()]')   #next page button
	next_button.click()
	time.sleep(2)
csv_file.close()
driver.close()