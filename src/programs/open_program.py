import subprocess
from . import select_program_path


def Execute(program_to_open):
    program_path = select_program_path.Execute(program_to_open)
    subprocess.Popen([program_path])