import sqlite3 as sql
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

db = config['PROGRAMS']['DB_NAME']



def Execute(name):
	with sql.connect(db) as conn:
		sql = """SELECT path FROM programs WHERE name LIKE ?"""

		name = '%' + name + '%'

		c = conn.cursor()
		c.execute(sql, [name])

		record = c.fetchall()
		return record.first()
