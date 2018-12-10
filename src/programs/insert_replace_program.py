import sqlite3 as sql
import configparser

config = configparser.ConfigParser()
config.read('config.py')

db = config['PROGRAMS']['DB_NAME']


def Execute(name, path, user_defined):
    with sql.connect(db) as conn:
        sql_command = f"""
			INSERT OR IGNORE INTO programs(name, path, user_defined)
			VALUES ('{name}', '{path}', {user_defined});
			UPDATE programs SET path = '{path}', user_defined = {user_defined}
			WHERE name = '{name}';		
		"""
        c = conn.cursor()
        c.execute(sql_command)
        if (c.lastrowid != 0):
            print(name + " is in Programs Database!")
    conn.close()
