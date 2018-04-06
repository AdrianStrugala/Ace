import repository
import speech
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

class Controller (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def write(self, text):
        print (text)

    def create_database(self):       
        path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'
        path2 = 'C:\\Users\\' + getpass.getuser() + r'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs'

        repository.create_table()
        print("Created database")

        self.insert_programs_from_path(path)
        self.insert_programs_from_path(path2)

    def clear_database(self):       
        repository.clear_table()


    def insert_programs_from_path(self, path):
        for file in glob.iglob(path + '/**/*.lnk', recursive=True):
            fullpath = os.path.join(path, file)
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(fullpath)

            name = (file[file.rindex('\\') + 1:]).split(".", 1)[0]

            repository.insert_program(name, shortcut.Targetpath)


    def open_program(self, program_to_open):
        program_path = repository.get_program_path(program_to_open)
        subprocess.Popen([program_path])

    def close_program(self, program_to_close):
        for process in (process for process in psutil.process_iter() if program_to_close in process.name()):
            process.kill()


    def open_website(self, url_to_open):
        if(url_to_open[0] != 'w' or url_to_open[1] != 'w' or url_to_open[2] != 'w' or url_to_open[3] != '.'):
            url_to_open = "www." + url_to_open

        webbrowser.get('windows-default').open(url_to_open, new=0)
        
        
    def search_in_google(self, phrase_to_search):
        googleUrl = "http://google.com/?#q="

        webbrowser.get('windows-default').open(googleUrl+phrase_to_search, new=0)
                
