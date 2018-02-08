import sqlite3 as sql

db = 'programs.db'


def create_table():
    with sql.connect(db) as conn:
        sql_create_table = """ CREATE TABLE IF NOT EXISTS src (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            path text
                                        ); """

        try:
            c = conn.cursor()
            c.execute(sql_create_table)
            print("Created table " + db)
        except Exception as e:
            print(e)

    conn.close()


def insert_program(name, path):
    with sql.connect(db) as conn:
        sql_insert_row = """INSERT INTO src (name, path) VALUES (?, ?)"""

        try:
            c = conn.cursor()
            c.execute(sql_insert_row, (name, path))
            print("Inserted " + name)
            print(c.lastrowid)
        except Exception as e:
            print(e)

    conn.close()


def get_program_path(name):
    with sql.connect(db) as conn:
        select_program = """SELECT path FROM src WHERE name LIKE ?"""

        name = '%' + name + '%'
        try:
            c = conn.cursor()
            c.execute(select_program, [name])
            print("Inserted " + name)
            print(c.lastrowid)


            record = c.fetchall()

            filepath = record[0]
            print(filepath)

        except Exception as e:
            print(e)
