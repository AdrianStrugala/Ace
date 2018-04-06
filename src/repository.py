import sqlite3 as sql

db = 'programs.db'


def create_table():
    with sql.connect(db) as conn:
        sql_create_table = """ CREATE TABLE IF NOT EXISTS src (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            path text,
                                            UNIQUE(name, path)
                                        ); """

        c = conn.cursor()
        c.execute(sql_create_table)
            
    conn.close()


def clear_table():
    with sql.connect(db) as conn:
        sql_create_table = """ DELETE FROM src """

        c = conn.cursor()
        c.execute(sql_create_table)
            
    conn.close()


def insert_program(name, path):
    with sql.connect(db) as conn:
        sql_insert_row = """INSERT OR IGNORE INTO src (name, path) VALUES (?, ?)"""
       
        c = conn.cursor()
        c.execute(sql_insert_row, (name, path))
        if(c.lastrowid != 0):
            print("Inserted " + name " at " + c.lastrowid)

    conn.close()


def get_program_path(name):
    with sql.connect(db) as conn:
        select_program = """SELECT path FROM src WHERE name LIKE ?"""

        name = '%' + name + '%'

        c = conn.cursor()
        c.execute(select_program, [name])

        record = c.fetchall()
        return record[0]
