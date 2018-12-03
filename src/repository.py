import sqlite3 as sql

db = 'programs.db'


def create_table():
	with sql.connect(db) as conn:
		sql_create_table = """ 
		CREATE TABLE IF NOT EXISTS programs (
        id integer PRIMARY KEY,
        name text NOT NULL,
        path text,
        user_defined bit,
        UNIQUE(name, path));
        """

		c = conn.cursor()
		c.execute(sql_create_table)

	conn.close()


def clear_table():
	with sql.connect(db) as conn:
		sql_create_table = """ DELETE FROM programs """

		c = conn.cursor()
		c.execute(sql_create_table)

	conn.close()


def insert_program(name, path, user_defined):
	with sql.connect(db) as conn:
		sql_command = f"""
		MERGE programs as [Target] 
		USING  (VALUES ('{name}', '{path}', {user_defined})) as [Source]
		(name, path, user_defined)
		ON [Target].name = [Source].name
		WHEN MATCHED THEN
			UPDATE [Target]
			SET name = '{name}', path = '{path}', user_defined = {user_defined};
		WHEN NOT MATCHED THEN
			INSERT (name, path, user_defined)
			VALUES ('{name}', '{path}', {user_defined});
		"""
		c = conn.cursor()
		c.execute(sql_command)
		if(c.lastrowid != 0):
			print('Added ' + name + ". Number of programs: " + str(c.lastrowid))
	conn.close()


def get_program_path(name):
	with sql.connect(db) as conn:
		sql = """SELECT path FROM programs WHERE name LIKE ?"""

		name = '%' + name + '%'

		c = conn.cursor()
		c.execute(sql, [name])

		record = c.fetchall()
		return record[0]
