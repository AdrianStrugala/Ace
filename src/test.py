import os
import subprocess
import sys
import win32com.client
import getpass
import glob

# path = r'C:\Users\strugala\AppData\Roaming\Microsoft\Windows\Start Menu\Programs'
path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'

# for file in os.listdir(path):
for file in glob.iglob(path + '/**/*.lnk', recursive=True):
    #   if file.endswith(".lnk"):
    print(file)
    fullpath = os.path.join(path, file)

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(fullpath)

    name = (file[file.rindex('\\')+1:]).split(".", 1)[0]

    print(name)
    print(shortcut.Targetpath)

print(getpass.getuser())

path2 = 'C:\\Users\\' + getpass.getuser() + r'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs'

print(path2)

for file in os.listdir(path2):
    if file.endswith(".lnk"):
        fullpath = os.path.join(path2, file)

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(fullpath)

        name = file.split(".", 1)[0]

        print(name)
        print(shortcut.Targetpath)
# print (fullpath)
# subprocess.Popen([fullpath])
