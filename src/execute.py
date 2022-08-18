from getpass import getpass
from time import sleep
import psutil
from threading import Thread

from utils import priority_handler
from win32api import ChangeDisplaySettings
from utils import get_active_window, display_mode


def parse_n_run(namespace):
    exe = namespace.e
    dm = namespace.dm
    pri = namespace.p

    print(f'''
Executable: {exe}
Display mode: {dm}
Priority: {pri.lower().capitalize()}''')

    process = psutil.Popen(exe)
    if pri is not None:
        process.nice(priority_handler(pri))
    Thread(target=check_process, args=(process.is_running, )).start()
    if dm != None:
        display_mode_handler(exe, dm).apply()


def check_process(check: bool):
    while True:
        if check() is False:
            exit()
        sleep(0.1)


class display_mode_handler():
    """
    Display Mode Handler
    """

    def __init__(self, exe, dm) -> None:
        self.exe = exe
        self.dm = dm

    def apply(self):
        apply = False
        while True:
            try:
                sleep(0.1)
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
                sleep(0.1)
                if self.exe != get_active_window():
                    reset = True

                if reset:
                    ChangeDisplaySettings(None, 0)
                    break
            except (psutil.NoSuchProcess, ValueError):
                pass
        self.apply()
