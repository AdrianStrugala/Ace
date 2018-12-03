import getpass
import glob
import os
import win32com
from . import create_table
from . import insert_replace_program



def Execute():
	path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'
	path2 = 'C:\\Users\\' + getpass.getuser() + r'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs'

	create_table.Execute()

	populate_programs_from_path(path)
	populate_programs_from_path(path2)




def populate_programs_from_path(path):
	for file in glob.iglob(path + '/**/*.lnk', recursive=True):
		fullpath = os.path.join(path, file)
		shell = win32com.client.Dispatch("WScript.Shell")
		shortcut = shell.CreateShortCut(fullpath)

		name = (file[file.rindex('\\') + 1:]).split(".", 1)[0]

		insert_replace_program.Execute(name, shortcut.Targetpath, 0)




