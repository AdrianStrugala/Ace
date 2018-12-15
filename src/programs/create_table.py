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

	# Revert current working directory
	os.chdir(original_cwd)
