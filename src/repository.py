import sqlite3 as sql

db = 'programs.db'



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


def get_program_path(name):
	with sql.connect(db) as conn:
		sql = """SELECT path FROM programs WHERE name LIKE ?"""

		name = '%' + name + '%'

		c = conn.cursor()
		c.execute(sql, [name])

		record = c.fetchall()
		return record[0]
