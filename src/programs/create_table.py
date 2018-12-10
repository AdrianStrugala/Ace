import sqlite3 as sql
import configparser


config = configparser.ConfigParser()
config.read('config.py')

db = config['PROGRAMS']['DB_NAME']



def Execute():
	with sql.connect(db) as conn:
		sql_create_table = """
		CREATE TABLE IF NOT EXISTS programs (
        id integer PRIMARY KEY,
        name text NOT NULL,
        path text,
        user_defined bit);    
        """

		sql_create_index = """CREATE UNIQUE INDEX IF NOT EXISTS idx_programs_name ON programs (name);"""

		c = conn.cursor()
		c.execute(sql_create_table)
		c.execute(sql_create_index)

	conn.close()