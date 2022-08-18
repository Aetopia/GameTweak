from os import _exit
from threading import Thread
from time import sleep

import psutil
from win32api import ChangeDisplaySettings

from utils import *


def parse_n_run(namespace):
    # For some reason, each argument is stored as a list in the namespace. (I will likely fix this in a future update.)
    exe = namespace.executable[0]
    dm = namespace.displaymode[0]
    pri = namespace.priority[0]
    process_check = False
    delay = autodelay()

    print(f'''
Executable: {str(exe)}
Display Mode: {str(dm)}
Priority: {str(pri).lower().capitalize()}''')

    process = psutil.Popen(exe)

    if pri:
        process.nice(priority_class(pri))

    if dm:
        """
        Isolates the Display Mode Handler in a separate thread.
        """
        Thread(target=display_mode_handler, args=(exe, dm)).start()
        process_check = True
    
    if process_check:
        while True:
            if process.is_running() is False:
                _exit(0)
            sleep(delay)
    
    


class display_mode_handler():
    """
    Display Mode Handler
    """

    def __init__(self, exe, dm) -> None:
        self.exe = exe
        self.dm = dm
        self.delay = autodelay()
        self.apply()

    def apply(self):
        apply = False
        while True:
            try:
                sleep(self.delay)
                if self.exe == get_active_window():
                    apply = True

                if apply:
                    ChangeDisplaySettings(display_mode(self.dm), 0)
                    break
            except (psutil.NoSuchProcess, ValueError):
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
            except (psutil.NoSuchProcess, ValueError):
                pass
        self.apply()
