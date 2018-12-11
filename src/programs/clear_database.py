import sqlite3 as sql
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

db = config['PROGRAMS']['DB_NAME']


def Execute():
	with sql.connect(db) as conn:
		sql_create_table = """ DELETE FROM programs """

		c = conn.cursor()
		c.execute(sql_create_table)

	conn.close()