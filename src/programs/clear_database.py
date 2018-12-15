import sqlite3 as sql
import configparser
import os
original_cwd = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

config = configparser.ConfigParser()
config.read('..\config.ini')

db = config['PROGRAMS']['DB_NAME']


def Execute():
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	with sql.connect(db) as conn:
		sql_create_table = """ DELETE FROM programs """

		c = conn.cursor()
		c.execute(sql_create_table)

	conn.close()

	# Revert current working directory
	os.chdir(original_cwd)
