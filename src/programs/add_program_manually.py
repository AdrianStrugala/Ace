import tkinter as tk
from tkinter import filedialog

from programs import insert_replace_program

def Execute():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                           filetypes=(("exe files", "*.exe"), ("all files", "*.*")))
    print("Selected program location: " + file_path)
    name = input('Type name or alias of the program: ')

    insert_replace_program.Execute(name, file_path, 1)