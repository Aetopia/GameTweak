from argparse import Namespace
from os import _exit
from sys import exit
from threading import Thread
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
        Thread(target=child_procs_priority, args=(
            proc, pri), name='child_procs_priority').start()

    if dm:
        """
        Isolates the Display Mode Handler in a separate thread.
        """
        Thread(target=display_mode_handler, args=(
            exe, dm, delay, proc), name='display_mode_handler').start()
        proc_check = True

    if proc_check:
        Thread(target=is_proc_running, args=(
            proc,), name='is_proc_running').start()


def is_proc_running(proc):
    while True:
        if not proc.is_running():
            sleep
            _exit(0)


def child_procs_priority(proc, priority):
    """
    Set the priority of the child processes of a process.
    """
    child_procs = proc.children
    _ = True
    i = 0
    while _:
        if child_procs() != []:
            _ = False
            for child in child_procs(recursive=True):
                try:
                    Process(child.pid).nice(priority)
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass
        sleep(1)
        i += 1
        if i == 60:
            exit(0)


class display_mode_handler():
    """
    Display Mode Handler
    """

    def __init__(self, exe: str, dm: str, delay: int, proc) -> None:
        self.exe = exe
        self.dm = display_mode(dm)
        self.delay = delay
        self.proc = proc
        self.exceptions = psutil.NoSuchProcess, ValueError
        self.apply()

    def apply(self):
        apply = False
        exes = self.exe + [child.name for child in self.proc.children()]
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
        exes = self.exe + [child.name for child in self.proc.children()]
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
