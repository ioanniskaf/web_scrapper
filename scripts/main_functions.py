import constants
from datetime import datetime
import pandas as pd  
import os
import re

def clean_mileage(dfs):
	def correct_mileage(x):
		if x > 1 and x < 1000:
			return x*1000
		elif x <= 1:
			return 0
		else:
			return x
	dfs = dfs.apply(lambda x: re.sub('[^\d]','',str(x)))
	dfs = pd.to_numeric(dfs)
	dfs = dfs.apply(lambda x: correct_mileage(x))
	return dfs

def clean_hp(dfs):
	dfs = dfs.apply(lambda x: re.sub('[^\d]','',str(x)))
	dfs = pd.to_numeric(dfs)
	return dfs

def clean_year(dfs):
	def categorize(x):
		if x <=1995:	# 206 Cars
			return '< 1995'
		elif x > 1995 and x <= 2002:	# 723 Cars
			return '1995 - 2002'
		elif x > 2002 and x <= 2006:	# 913 Cars
			return '2002 - 2006'
		elif x > 2006 and x <= 2009:	# 944 Cars
			return '2006 - 2009'
		elif x > 2009 and x <= 2014:	# 1434 Cars
			return '2009 - 2014'
		elif x > 2014 and x <= 2016:	# 1466 Cars
			return '2014 - 2016'
		elif x > 2016 and x <= 2019:	# 1892 Cars
			return '2016 - 2019'
		else:	# 206 Cars
			return '> 2020'
	dfs = pd.to_numeric(dfs, downcast='integer')
	dfs = dfs.apply(lambda x: categorize(x))
	dfs = dfs.astype(str)
	return dfs

def clean_brand(dfs):
	def brand_to_country(brand):
		if brand in constants.brand_country:
			return constants.brand_country[brand]
		else:
			return 'unknown'
	dfs = dfs.apply(lambda x: brand_to_country(x))
	return dfs

def clean_price(dfs):
	dfs = dfs.apply(lambda x: re.sub('[^\d]','',str(x)))
	dfs = pd.to_numeric(dfs)
	return dfs

def clean_extras(extras):
	res = map(lambda x: re.sub('(\\\\\\\\u002F)','' ,x), extras)
	res = map(lambda x: re.sub('[^\w_-]','' ,x), list(res))
	return list(res)

def getUniqueExtrasDict(fpath, filename):
	df = df.apply(lambda x: x.split(','))
	df = df.apply(lambda x: clean_extras(x))
	return df

def concat_csv_files_to_df(fpath):
	'''
	Recursively goes through the root directory and
	reads and concatenates all csv files in a single DataFrame
	then return it.
	'''
	df = pd.DataFrame()
	for root, dir, files in os.walk(fpath):
		for fname in files:
			if '.csv' in fname:
				#print(root, fname)
				df_temp = pd.read_csv(root + '/' + fname)
				df = pd.concat([df,df_temp], ignore_index=True)
	return df

def clean_df_and_write_to_file(df, fpath, filename):
	df = df.rename(columns=constants.columns_rename)

	# Drop duplicates, with same link id
	df.drop_duplicates(subset=['id'], inplace=True)

	# Drop empty info cars (not downloaded or errors)
	df.dropna(how='all', inplace=True)

	# Write back and replace output file
	#df.to_csv(fpath + filename, index=False)
	return df