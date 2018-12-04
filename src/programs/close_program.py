import psutil


def Execute(program_to_close):
    for process in (process for process in psutil.process_iter() if program_to_close in process.name()):
        process.kill()