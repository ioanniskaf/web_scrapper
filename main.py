from scripts.main_functions import *

def main():
	# Root , where the csv files are located
	root = 'output/cars/'
	folder = 'links_04'

	#df = concat_csv_files_to_df(root + folder)
	df = pd.read_csv('output.csv')

	# Timestamp to be used as in output filename as id
	#timestamp = datetime.timestamp(datetime.now())
	#timestamp = int(1000*timestamp)
	# Filename to be used as concatenated output.
	#filename = 'output_' + folder + '_' + str(timestamp) + '.csv'

	df = clean_df_and_write_to_file(df, root, '') #Rename Columns, drop duplicates, drop empty

	df['year'] = clean_year(df['year'])

	df['id']=pd.to_numeric(df['id'], downcast="integer").astype(str)

	df['price'] = clean_price(df['price'])

	df['state'] = df['state'].apply(lambda x: 'new' if(pd.isna(x)) else 'used')

	df['brand'] = clean_brand(df['brand'])
	df = df.rename(columns={'brand':'country'})

	df['mileage'] = clean_mileage(df['mileage'])

	df['hp'] = clean_hp(df['hp'])

	print(df.info())
	print(df.hp.head(50))

main()