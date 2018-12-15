import sqlite3 as sql
import configparser
import os
original_cwd = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

config = configparser.ConfigParser()
config.read('..\config.ini')

db = config['PROGRAMS']['DB_NAME']


def Execute(name, path, user_defined):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    with sql.connect(db) as conn:
        sql_command = f"""
			INSERT OR IGNORE INTO programs(name, path, user_defined)
			VALUES ('{name}', '{path}', {user_defined});
			UPDATE programs SET path = '{path}', user_defined = {user_defined}
			WHERE name = '{name}';		
		"""
        c = conn.cursor()
        c.executescript(sql_command)
        if (c.lastrowid != 0):
            print(name + " is in Programs Database!")
    conn.close()

    # Revert current working directory
    os.chdir(original_cwd)
