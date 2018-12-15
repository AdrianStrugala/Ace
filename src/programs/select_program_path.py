import sqlite3 as sql
import configparser
import os
original_cwd = os.getcwd()

config = configparser.ConfigParser()
config.read('..\config.ini')

db = config['PROGRAMS']['DB_NAME']



def Execute(name):
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	with sql.connect(db) as conn:
		sql_command = """SELECT path FROM programs WHERE name LIKE ?"""

		name = '%' + name + '%'

		c = conn.cursor()
		c.execute(sql_command, [name])

		record = c.fetchall()
		return record[0]

	# Revert current working directory
	os.chdir(original_cwd)
