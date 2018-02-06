import sqlite3 as sql
import winreg
import subprocess
import glob, os


def create_table(conn):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS programs (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        path text
                                    ); """

    try:
        c = conn.cursor()
        c.execute(sql_create_table)
        print("Created table programs")
    except Exception as e:
        print(e)


def insert_row(conn, name, path):
    sql_insert_row = """INSERT INTO programs (name, path) VALUES (?, ?)"""

    try:
        c = conn.cursor()
        c.execute(sql_insert_row, (name, path))
        print("Inserted " + name)
        print(c.lastrowid)
    except Exception as e:
        print(e)

def subkeys(key):
    i = 0
    while True:
        try:
            subkey = winreg.EnumKey(key, i)
            yield subkey
            i += 1
        except WindowsError as e:
            break

if __name__ == '__main__':
    with sql.connect('test.db') as conn:
        create_table(conn)


        keypath = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)

        aKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keypath, 0, winreg.KEY_READ)
        for subkeyname in subkeys(aKey):

            thiskey = keypath + "\\" + subkeyname
            thisSubKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, thiskey, 0, winreg.KEY_READ)

            path = ''
            try:
                path = winreg.QueryValueEx(thisSubKey, "InstallLocation")[0]
            except:
                path = ''
            if path != '':
                try:
                    filepath = os.chdir(winreg.QueryValueEx(thisSubKey, "InstallLocation")[0])
                    for file in glob.glob("*.exe"):
                        print(file)

                    insert_row(conn, winreg.QueryValueEx(thisSubKey, "DisplayName")[0], winreg.QueryValueEx(thisSubKey, filepath+ "\\" +file)[0])
                except:
                    None


        c = conn.cursor()
        c.execute("SELECT * FROM programs")
        rows = c.fetchall()

        new_query = """SELECT path FROM programs WHERE name LIKE ?"""

        c = conn.cursor()

        program = 'Chrome'

        c.execute(new_query, ['%'+program+'%'])

        record = c.fetchall()[0]

        filepath = record[0]
        print (filepath)


        os.chdir(filepath)
        for file in glob.glob("*.exe"):
            print (file)

        program = filepath+ "\\" +file
        print(program)
        subprocess.Popen([program])