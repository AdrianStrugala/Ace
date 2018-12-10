import sqlite3 as sql
import configparser


config = configparser.ConfigParser()
config.read('config.py')

db = config['PROGRAMS']['DB_NAME']



def Execute(name):
	with sql.connect(db) as conn:
		sql_command = """SELECT path FROM programs WHERE name LIKE ?"""

		name = '%' + name + '%'

		c = conn.cursor()
		c.execute(sql_command, [name])

		record = c.fetchall()
		return record[0]
