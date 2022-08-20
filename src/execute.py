from argparse import Namespace
from os import _exit
from threading import Thread
from time import sleep

import psutil
from win32api import ChangeDisplaySettings

from utils import *


def parse_n_run(namespace: Namespace):
    exe = namespace.executable
    dm = namespace.displaymode
    pri = namespace.priority
    launch = namespace.launcher
    process_check = False
    delay = autodelay()

    print(f'''
Executable: {str(exe)}
Display Mode: {str(dm)}
Priority: {str(pri).lower().capitalize()}''')

    process = psutil.Popen(exe)

    if pri:
        pri = priority_class(pri)
        process.nice(pri)
        if launch:
            child_procs_priority(process, pri)

    if dm:
        """
        Isolates the Display Mode Handler in a separate thread.
        """
        Thread(target=display_mode_handler, args=(exe, dm, delay)).start()
        process_check = True

    if process_check:
        while True:
            if process.is_running() is False:
                sleep(1)
                _exit(0)
            sleep(delay)


def child_procs_priority(process, priority):
    """
    Set the priority of the child processes of a process.
    """
    child_procs = process.children
    _ = True
    while _:
        if child_procs() != []:
            _ = False
            for child in child_procs(recursive=True):
                try:
                    Process(child.pid).nice(priority)
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass

        sleep(0.001)
    

class display_mode_handler():
    """
    Display Mode Handler
    """

    def __init__(self, exe: str, dm: str, delay: int) -> None:
        self.exe = exe
        self.dm = display_mode(dm)
        self.delay = delay
        self.exceptions = psutil.NoSuchProcess, ValueError
        self.apply()

    def apply(self):
        apply = False
        while True:
            try:
                sleep(self.delay)
                if self.exe == get_active_window():
                    apply = True

                if apply:
                    ChangeDisplaySettings(self.dm, 0)
                    break
            except (self.exceptions):
                pass
        self.reset()

    def reset(self):
        reset = False
        while True:
            try:
                sleep(self.delay)
                if self.exe != get_active_window():
                    reset = True

                if reset:
                    ChangeDisplaySettings(None, 0)
                    break
            except (self.exceptions):
                pass
        self.apply()
