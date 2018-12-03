import sqlite3 as sql
import configparser
import getpass
import glob
import os
import win32com

config = configparser.ConfigParser()
config.read('../config.ini')

db = config['PROGRAMS']['DB_NAME']


def Execute():
    path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'
    path2 = 'C:\\Users\\' + getpass.getuser() + r'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs'

    Create_table()

    insert_programs_from_path(path)
    insert_programs_from_path(path2)


def Create_table():
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


def insert_programs_from_path(path):
    for file in glob.iglob(path + '/**/*.lnk', recursive=True):
        fullpath = os.path.join(path, file)
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(fullpath)

        name = (file[file.rindex('\\') + 1:]).split(".", 1)[0]

        insert_program(name, shortcut.Targetpath, 0)


def insert_program(name, path, user_defined):
	with sql.connect(db) as conn:
		sql_command = f"""		
			REPLACE INTO programs (name, path, user_defined)
			VALUES ('{name}', '{path}', {user_defined});
		"""
		c = conn.cursor()
		c.execute(sql_command)
		if(c.lastrowid != 0):
			print(name + " is in Programs Database!")
	conn.close()