import repository
import subprocess
import psutil
import threading
import tkinter as tk
from tkinter import filedialog


class Controller (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def write(self, text):
        print (text)



    def add_program_manually(self):       
        root = tk.Tk()
        root.withdraw()

        file_path =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("exe files","*.exe"),("all files","*.*")))
        print ("Selected program location: " + file_path)
        name = input('Type name or alias of the program: ')

        repository.insert_program(name, file_path, 1)


    def clear_database(self):       
        repository.clear_table()


    def open_program(self, program_to_open):
        program_path = repository.get_program_path(program_to_open)
        subprocess.Popen([program_path])


    def close_program(self, program_to_close):
        for process in (process for process in psutil.process_iter() if program_to_close in process.name()):
            process.kill()
           
                
