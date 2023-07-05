import re
import requests
from time import sleep
from bs4 import BeautifulSoup
from constants.headers import headers_, user_agent_
from scripts.reboot_router import reboot_router
import csv
import json

def clean(link):
	link = link.strip()
	link = link.replace('?from-promotion=1','')
	return link

def readLinksFromFile(file):
	'''
	Takes as argument a .csv file and returns a list with all the links in the file
	'''
	with open(file,'r') as f:
		links = f.readlines()

	# Remove \n from each line
	
	links = [clean(link) for link in links]

	print('Links retrieved from ',f.name)
	
	return links

def requestCarInfoPage(car_link, max_attempts):
	site = 'https://www.car.gr/'
	page_url = site + car_link
	#page_url = site + car_link + '?lang=en'

	page = requests.get(page_url,timeout=10, headers = headers_)
	print(f'Processing Page Status Code: {page.status_code}')

	# attempt = 0
	# while attempt < max_attempts:
	# 	page = requests.get(page_url,timeout=10, headers = headers_)
	# 	print(f'Processing Page Status Code: {page.status_code}')
	# 	if page.status_code == 200:
	# 		attemts = max_attempts
	# 	else:
	# 		attemts +=1
	# 		if attempt != max_attempts:
	# 			reboot_router_(0)
	return page

def handleExtras(extras):
	extras_list = []
	temp_list = extras.split(',')
	for extra in temp_list:
		if 'name:' in extra:
			extra = re.sub(r'name:"','',extra)
			extra = re.sub(r'[{}"]','',extra)
			extras_list.append(extra)
	return extras_list

def getCarInfoFromLink(car_link):
	car_info = {}

	try:
		for req in range(0,3):
			page = requestCarInfoPage(car_link,2)
			if (page.status_code == 200):
				soup = BeautifulSoup(page.content, "html.parser")
				break
			elif (page.status_code == 429):
				reboot_router_()
				print('Page Error Code 429, Attempt: ', req+1)
				return car_info
			else:
				return car_info
		ul_class = r'\bc-breadcrumbs\b'
		ul = soup.find('ul', class_ = re.compile(ul_class))
		li_class = r'\bc-breadcrumb\b'
		li = soup.find_all('li', class_ = re.compile(li_class))
		car_info['brand'] = re.sub(r'\s+','', li[3].text)
		car_info['model'] = re.sub(r'\s+','', li[4].text)
		car_info['year'] = re.sub(r'\s+','', li[5].text)
		car_info['title'] = re.match(r'\s+(\w.*\w)\s+',li[6].text).group(1)
		table_div = soup.find('div', id = 'specification-table')
		table_rows = table_div.findChildren('tr')
		for tr in table_rows:
			cat=''
			info=''
			tds = tr.findChildren('td')
			for td in tds:
				if len(td.findChildren('span')) == 0:
					cat = re.sub(r'\s+','',td.text)
				else:
					info = re.sub(r'\s+','',td.text)				
			car_info[cat] = info
		scripts = soup.find_all('script')
		pattern = re.compile(r'.*,extras:\[(.*?)\]')
		for script in scripts:
			if "window.__NUXT__=" in script.text[:20]:
				extras = re.match(pattern, script.text).group(1)
		car_info['extras'] = handleExtras(extras)
		#print(car_info['extras'])
		return car_info

	except Exception as e:
		print('Error while getting car info: ' , e)
		return car_info

def getCarsKeys(cars):
	initial_keys = list(cars[0].keys())
	
	for car in cars:
	 	for key in car.keys():
 			if key not in initial_keys:
	 			initial_keys.append(key)
	
	dict_keys = initial_keys
	
	return dict_keys


def scrapCarsInfo(links_file,max_iterations,step,start):
	current_iteration = 0

	links = readLinksFromFile(links_file)
	links = links[start:]
	links_len = len(links)
	links_parsed = []

	while current_iteration < max_iterations:
		try:
			cars = []

			start = current_iteration * step
			if start > links_len-1:
				print('Reached EOF')
				break
			end = start + step
			if end > links_len:
				end = links_len

			sub_links = links[start:end]
			for idx,link in enumerate(sub_links):
				if link not in links_parsed:
					car = getCarInfoFromLink(link)
					sleep(3)
					cars.append(car)
					links_parsed.append(link)
					print(f'Cars Parsed:[{len(cars)}] - Iter:[{current_iteration}] - Link:[{idx}] > {link}')
				else:
					print('Link aleady parsed...')
				
			keys = getCarsKeys(cars)
			with open('./output/cars/cars_' + str(current_iteration) + '.csv', \
						'w+', encoding='utf-8', newline='') \
			as output_file:	
				dict_writer = csv.DictWriter(output_file,fieldnames=keys)
				dict_writer.writeheader()
				dict_writer.writerows(cars)
			current_iteration+=1
			print(f'******************{step} cars indexed!!!******************')
		except Exception as e:
			current_iteration+=1
			print('Error while parsign cara data: ', e)
			continue