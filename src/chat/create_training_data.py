import pandas
import sqlite3
import configparser
import os
original_cwd = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

config = configparser.ConfigParser()
config.read('..\config.ini')

db = config['CHAT']['DB_NAME']
batch_size = 1000
data_folder = "./AI_nmt/new_data"

def Execute():
	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	connection = sqlite3.connect(db)
	last_unix = 0
	current_length = batch_size
	counter = 0

	while current_length > 0:
		dataframe = pandas.read_sql(f"""
									SELECT * FROM parent_reply 
									WHERE unix > {last_unix} and parent != ''
									ORDER BY unix ASC
									LIMIT {batch_size}
									""", connection)
		current_length = len(dataframe)
		if current_length > 0:
			last_unix = dataframe.tail(1)['unix'].values[0]

			with open(f"{data_folder}/train.from", 'a', encoding='utf8') as file:
				for content in dataframe['parent'].values:
					file.write(content + '\n')
			with open(f"{data_folder}/train.to", 'a', encoding='utf8') as file:
				for content in dataframe['comment'].values:
					file.write(content + '\n')

			counter +=1
		if counter % 20 == 0:
			print(str(counter * batch_size) + ' rows complited so far')

	# Revert current working directory
	os.chdir(original_cwd)
