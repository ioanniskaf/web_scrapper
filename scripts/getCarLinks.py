import re
import requests
from time import sleep
from bs4 import BeautifulSoup
from constants.headers import headers_, user_agent_
from scripts.reboot_router import reboot_router

def getLinksFromPages(start, num_of_pages,max_attempts):
	'''
	Retrieves the car links available in each from car.gr pages
	Takes as arguments the starting page and the total number of pages
	we need to parse. Max attempts per page can be passed as argument.
	'''
	car_links = []
	site = "https://www.car.gr/" 
	
	for i in range(start,start + num_of_pages):
		try:
			attempt = 0
			while attempt < max_attempts:
				# We can use the below random user agent if needed
				# headers =  {'User-Agent': user_agent()_}

				# For ordered by Creation Date pages
				page_url = site + "classifieds/cars/?pg=" + str(i) + "&sort=cr"
				page = requests.get(page_url,timeout=10, headers = headers_)

				# If 200 OK returned as response
				if page.status_code == 200:
					soup = BeautifulSoup(page.content, "html.parser")

					# Links are located inside <div> with class="search-row swipable"
					car_div = r"\bsearch-row swipable\b"
					cars = soup.find_all("div", class_ = re.compile(car_div))

					# Above returns all car links in the page
					# Iterate and append to list
					for car in cars:
						car_link = car.find("a", class_ = "row-anchor")
						car_links.append(car_link["href"])

					print(f'Processing Page : {i:>3} | Links registered: {len(car_links)}')
					attempt = max_attempts # Exit loop
					
					# Sleep to avoid Too many requests responses
					sleep(4)
				elif page.status_code == 429: #Too many requests
					print(f'Processing Page Status Code: {page.status_code}')
					reboot_router(10)
					attempt += 1
				else:
					# If status code is different, log and try again
					print(f'Processing Page Status Code: {page.status_code}')
					attempt += 1
		except Exception as e:
			# Catch and display any errors
			print(f'Processing Page : {i:>3} Failed  {e} \n')
			continue
	
	return car_links

def writeLinksToFile(car_links, file):
	'''
	Takes as arguments a list and a file and writes the list items
	in each line of the file.
	'''
	if len(car_links) > 0:
		with open(file,"w") as f:
			for car_link in car_links:
				f.write(car_link + "\n")
		print("Link file has been created")
	else:
		print("Cannot write empty list on file")


def getLinks(mode, path, prefix, iterations, start, step):
	'''
	Main function.Each page contains 26 links. For the number of
	iterations specified get links located in pages from 
	start to start + step and write those links to a csv file
	with the prefix given to the path given as input or return list or both.

	Modes:
	 (0) : Creates csv file per iteration
	 (1) : Returns list after all iterations completed
	 (2) : Modes 0 and 1 combined

	Example:
	getLinks(0, "./test/", "test_", 5, 1, 100)
	--->This will create 5 csv files each containing links from 100 pages
	starting from page 1 (1-100 , 101-200 , 201-300 , 301-400, 401-500)
	Each csv file will have 2600 links (100 pages * 26 links/page)
	Total  5 * 2600 links will be registered.
	'''
	links = []

	if mode > 2:
		print("Error: getLinks mode can only be 0,1 or 2")
	else:
		for i in range(0,iterations):
			car_links = getLinksFromPages(start+i*step, step, max_attempts = 3)
			fpath = path + prefix + str(i) + ".csv"
			if mode == 0:
				writeLinksToFile(car_links, fpath)
			elif mode == 1:
				links.append(car_links)
			elif mode == 2:
				writeLinksToFile(car_links, fpath)
				links.append(car_links)
	return links