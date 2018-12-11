import pandas
import sqlite3
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

db = config['CHAT']['DB_NAME']
batch_size = 1000

def Execute():

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

			with open("./chat/temp/train.from", 'a', encoding='utf8') as file:
				for content in dataframe['parent'].values:
					file.write(content + '\n')
			with open("./chat/temp/train.to", 'a', encoding='utf8') as file:
				for content in dataframe['comment'].values:
					file.write(content + '\n')

			counter +=1
		if counter % 20 == 0:
			print(str(counter * batch_size) + ' rows complited so far')
