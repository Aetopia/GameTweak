from time import sleep
from psutil import (ABOVE_NORMAL_PRIORITY_CLASS, HIGH_PRIORITY_CLASS,
                    NORMAL_PRIORITY_CLASS, Process, NoSuchProcess)
from utils import *
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
        self.exceptions = NoSuchProcess, ValueError
        pass

    def apply(self):
        apply = False
        while True:
            try:
                sleep(self.delay)
                hook, hooked_process = winhook().get_hook(), winhook().hook_process()
                if hook is not None:
                    pri = hook.split(',')[0]
                    _, _, pid = hooked_process
                    apply = True

                if apply is True:
                    pri_class = priority_class(pri)
                    process = Process(pid)
                    if process.nice() != pri_class:
                        process.nice(pri_class)
                    apply = False
            except (self.exceptions):
                pass

    def thread(self):
        error_handler(self.apply)
