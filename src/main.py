import os
import repository
import subprocess
import winreg


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

    repository.create_table()

    key_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
    aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)

    aKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
    for sub_key_name in subkeys(aKey):

        this_key = key_path + "\\" + sub_key_name
        thisSubKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, this_key, 0, winreg.KEY_READ)

        path = ''
        try:
            path, regtype = winreg.QueryValueEx(thisSubKey, "InstallLocation")
        except:
            path = ''
        if path != '':
            try:
                for file in os.listdir(path):
                    if file.endswith(".exe"):
                        fullpath = os.path.join(path, file)
                        print(fullpath)

                        repository.insert_program(winreg.QueryValueEx(thisSubKey, "DisplayName")[0], fullpath)
            except:
                None

    program = "%" + "Chrome" + "%"

    #
    #     subprocess.Popen([program])
    # except Exception as e:
    #     print(e)

# os.chdir(filepath)
# for file in glob.glob("*.exe"):
#     print(file)
#
# program = filepath + "\\" + file
# print(program)
# except Exception as e:
