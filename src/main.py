import repository
import subprocess
import winreg
import os
import subprocess
import sys
import win32com.client
import getpass
import glob



def insert_programs_from_path(path):
    for file in glob.iglob(path + '/**/*.lnk', recursive=True):
        fullpath = os.path.join(path, file)
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(fullpath)

        name = (file[file.rindex('\\') + 1:]).split(".", 1)[0]

        repository.insert_program(name, shortcut.Targetpath)


if __name__ == '__main__':

    path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'
    path2 = 'C:\\Users\\' + getpass.getuser() + r'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs'

    repository.create_table()

    insert_programs_from_path(path)
    insert_programs_from_path(path2)

    program_path = repository.get_program_path('Chrome')
    subprocess.Popen([program_path])