from argparse import Namespace
from os import _exit
from sys import exit
import threading as td
from time import sleep

import psutil
from win32api import ChangeDisplaySettings

from utils import *

"""
Thread handle themselves.
"""


def parse_n_run(namespace: Namespace):
    exe = namespace.executable
    dm = namespace.displaymode
    pri = namespace.priority
    delay = autodelay()
    proc_check = False

    print(f'''
Executable: {str(exe)}
Display Mode: {str(dm)}
Priority: {str(pri).lower().capitalize()}''')

    proc = psutil.Popen(exe)

    if pri:
        pri = priority_class(pri)
        proc.nice(pri)
        td.Thread(target=child_procs_priority, args=(
            proc, pri), name='child_procs_priority').start()

    if dm:
        """
        Isolates the Display Mode Handler in a separate thread.
        """
        td.Thread(target=display_mode_handler, args=(
            exe, dm, delay, proc), name='display_mode_handler').start()
        proc_check = True

    if proc_check:
    # Executes when GameTweak needs to monitor if a process is still running or not.
        while True:
            if not proc.is_running():
                sleep(1)
                _exit(0)
            sleep(1)
    else:
    # Executes when GameTweak doesn't need to monitor anything.
        for thread in td.enumerate():
            if thread.name != 'MainThread':
                thread.join()
        exit(0)



def child_procs_priority(proc, priority):
    """
    Set the priority of the child processes of a process.
    """
    child_procs = proc.children

    for _ in range(61):
        if child_procs() != []:
            for child in child_procs(recursive=True):
                try:
                    Process(child.pid).nice(priority)
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass
            break
        sleep(1)


class display_mode_handler():
    """
    Display Mode Handler
    """

    def __init__(self, exe: str, dm: str, delay: int, proc) -> None:
        self.exes = lambda: [exe] + \
            [child.name for child in proc.children()]
        self.dm = display_mode(dm)
        self.delay = delay
        self.exceptions = psutil.NoSuchProcess, ValueError
        self.apply()

    def apply(self):
        apply = False
        exes = self.exes()
        while True:
            try:
                sleep(self.delay)
                if get_active_window() in exes:
                    apply = True

                if apply:
                    ChangeDisplaySettings(self.dm, 0)
                    break
            except (self.exceptions):
                pass
        self.reset()

    def reset(self):
        reset = False
        exes = self.exes()
        while True:
            try:
                sleep(self.delay)
                if get_active_window() not in exes:
                    reset = True

                if reset:
                    ChangeDisplaySettings(None, 0)
                    break
            except (self.exceptions):
                pass
        self.apply()
