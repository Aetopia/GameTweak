from multiprocessing import cpu_count

from psutil import Process, HIGH_PRIORITY_CLASS, ABOVE_NORMAL_PRIORITY_CLASS, NORMAL_PRIORITY_CLASS
from win32gui import GetForegroundWindow
from win32process import GetWindowThreadProcessId
from pywintypes import DEVMODEType
from win32con import DM_PELSHEIGHT, DM_PELSWIDTH


def delay() -> float:
    """
    Returns a appropriate delay for the current CPU count.
    """
    cores = cpu_count()
    if cores in range(2,5):
        delay = 1.0
    else:
        delay = 0.1
    
    return delay

def get_active_window():
    """
    Get the executable name from an active window.
    """
    hwnd = GetForegroundWindow()
    pid = GetWindowThreadProcessId(hwnd)[1]
    return Process(pid).exe()


def display_mode(mode: str) -> DEVMODEType:
    """
    Parse the resolution string and return a DEVMODEType object.
    """
    w, h = mode.split('x')
    w, h = int(w.strip()), int(h.strip())
    res = DEVMODEType()
    res.PelsWidth, res.PelsHeight = w, h
    res.Fields = DM_PELSWIDTH | DM_PELSHEIGHT
    return res


def priority_class(priority):
    """
    Return a process class.
    """
    match priority.lower():
        case 'high':
            _class = HIGH_PRIORITY_CLASS
        case 'above_normal':
            _class = ABOVE_NORMAL_PRIORITY_CLASS
        case _:
            _class = NORMAL_PRIORITY_CLASS
    return _class
