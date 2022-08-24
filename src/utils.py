from multiprocessing import cpu_count
from traceback import format_exc
from win32api import MessageBox
from os import _exit

def auto_delay() -> float:
    """
    Returns a appropriate delay for the current CPU count.
    """
    cores = cpu_count()
    if cores in range(2,5):
        delay = 1.0
    else:
        delay = 0.1
    
    return delay

def error_handler(func):
    try:
        func()
    except Exception as e:
        MessageBox(0, format_exc(), str(e), 0)
        _exit(1)