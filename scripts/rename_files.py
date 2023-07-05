import os
from uuid import uuid4

def rename_files(from_path, to_path):
	'''
	Renames *.csv files in from_path (source) by adding a random uuid
	and moving them to to_path (destination) directory. If destination
	folder doesn't exists it creates one.
	'''
	files = 0

	if os.path.exists(from_path):
		if not os.path.exists(to_path):
			os.mkdir(to_path)
	
		for filename in os.listdir(from_path):
			if (".csv") in filename:
				id = str(uuid4())
				new_filename = "cars_" + id + ".csv"
				os.rename(from_path + filename, to_path + new_filename)

				print(f'File "{filename}" --> "{new_filename}" @ "{to_path}"')

				files+=1
		print(f'Total {files:>4} files renamed and moved.')
		return True
	else:
		print("The source folder doesn't exists.")
		return False
