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


def print_user_options():
    print("")
    print("Make your choice:")
    print("1 - Create Database")
    print("2 - Open Program")
    print("0 - Exit")


class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True


def case(*args):
    return any((arg == switch.value for arg in args))


if __name__ == '__main__':

    user_choice = 0

    while user_choice != -1:

        print_user_options()

        try:
            user_choice = int(input('Choice: '))
        except ValueError:
            print("Not a number")

        while switch(user_choice):
            if case(1):
                print("Creating Database...")
                path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'
                path2 = 'C:\\Users\\' + getpass.getuser() + r'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs'

                repository.create_table()

                insert_programs_from_path(path)
                insert_programs_from_path(path2)
                break

            if case(2):
                print("Opening Program...")
                program_to_open = input('Type name of the program: ')
                program_path = repository.get_program_path(program_to_open)
                subprocess.Popen([program_path])
                break

            if case(0):
                print("Exiting")
            print("Unrecognized option.")
            break
