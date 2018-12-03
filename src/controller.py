import repository
import subprocess
import winreg
import os
import subprocess
import sys
import win32com.client
import getpass
import glob
import webbrowser
import psutil
import threading
import tkinter as tk
from tkinter import filedialog


class Controller (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def write(self, text):
        print (text)


    def create_database(self):       
        path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'
        path2 = 'C:\\Users\\' + getpass.getuser() + r'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs'

        repository.create_table()

        self.insert_programs_from_path(path)
        self.insert_programs_from_path(path2)


    def add_program_manually(self):       
        root = tk.Tk()
        root.withdraw()

        file_path =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("exe files","*.exe"),("all files","*.*")))
        print ("Selected program location: " + file_path)
        name = input('Type name or alias of the program: ')

        repository.insert_program(name, file_path, 1)


    def clear_database(self):       
        repository.clear_table()


    def insert_programs_from_path(self, path):
        for file in glob.iglob(path + '/**/*.lnk', recursive=True):
            fullpath = os.path.join(path, file)
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(fullpath)

            name = (file[file.rindex('\\') + 1:]).split(".", 1)[0]

            repository.insert_program(name, shortcut.Targetpath, 0)


    def open_program(self, program_to_open):
        program_path = repository.get_program_path(program_to_open)
        subprocess.Popen([program_path])


    def close_program(self, program_to_close):
        for process in (process for process in psutil.process_iter() if program_to_close in process.name()):
            process.kill()
           
                
