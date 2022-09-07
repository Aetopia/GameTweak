from time import sleep

from pywintypes import error
from utils import *
from win32api import CloseHandle, OpenProcess
from win32con import PROCESS_ALL_ACCESS
from win32process import (ABOVE_NORMAL_PRIORITY_CLASS, HIGH_PRIORITY_CLASS,
                          NORMAL_PRIORITY_CLASS, GetPriorityClass,
                          SetPriorityClass)
from winhook import winhook


def priority_class(priority):
    """
    Return a priority class.
    """
    match priority.lower():
        case 'high':
            _class = HIGH_PRIORITY_CLASS
        case 'above normal':
            _class = ABOVE_NORMAL_PRIORITY_CLASS
        case 'normal':
            _class = NORMAL_PRIORITY_CLASS
    return _class


class handler():
    def __init__(self) -> None:
        self.delay = auto_delay()
        pass

    def apply(self):
        apply = False

        while True:
            try:
                sleep(self.delay)
                hook, hooked_process, hProc = winhook().get_hook(), winhook().hook_process(), 0

                if hook is not None:
                    pri = priority_class(hook.split(',')[0])
                    _, _, pid = hooked_process
                    hProc = OpenProcess(PROCESS_ALL_ACCESS, False, pid)
                    apply = True

                if apply is True:
                    if GetPriorityClass(hProc) != pri:
                        SetPriorityClass(hProc, pri)
                    apply = False

                if hProc != 0:
                    CloseHandle(hProc)
            except error:
                pass

    def thread(self):
        error_handler(self.apply)
