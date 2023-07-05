import pandas as pd  
import re

def clean(extras):
	res = map(lambda x: re.sub("(\\\\\\\\u002F)","" ,x), extras)
	res = map(lambda x: re.sub("[^\w_-]","" ,x), list(res))
	return list(res)

def getUniqueExtras(extras, uniqueExtrasDict):
	for extra in extras:
		# If not empty list
		if extra != '':
			if extra not in uniqueExtrasDict:
				uniqueExtrasDict[extra] = 1
			else:
				uniqueExtrasDict[extra] += 1

	return uniqueExtrasDict

def getUniqueExtrasDict(fpath, filename):
	'''
	Returns a dictionary with all the extras counted for all the
	cars in a specific file.
	'''
	uniqueExtrasDict = {}

	df = pd.read_csv(fpath + filename)
	
	# Split extras string into list items
	df["extras"] = df["extras"].apply(lambda x: x.split(","))
	
	# Clean each item
	df["extras"] = df["extras"].apply(lambda x: clean(x))
	
	# Add key:value pairs in dictionary if needed and count
	df["extras"].map(lambda x: getUniqueExtras(x,uniqueExtrasDict))

	return uniqueExtrasDict