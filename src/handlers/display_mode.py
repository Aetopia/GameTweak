from winhook import winhook
from psutil import NoSuchProcess
from pywintypes import DEVMODEType
from win32con import DM_PELSHEIGHT, DM_PELSWIDTH
from win32api import ChangeDisplaySettings
from time import sleep
from utils import auto_delay

def display_mode(mode: str) -> DEVMODEType:
    """
    Parse the resolution string and return a DEVMODEType object.
    """
    w, h = mode.split('x')
    w, h = int(w.strip()), int(h.strip())
    dm = DEVMODEType()
    dm.PelsWidth, dm.PelsHeight = w, h
    dm.Fields = DM_PELSWIDTH | DM_PELSHEIGHT
    return dm

class handler:
    """
    Display Mode Handler
    """
    def __init__(self) -> None:
        self.delay = auto_delay()
        self.exceptions = NoSuchProcess, ValueError

    def apply(self):
        apply = False
        while True:
            try:
                sleep(self.delay)
                hook = winhook().get_hook()

                if hook is not None:
                    dm = display_mode(hook.split(',')[1])
                    apply = True

                if apply:
                    ChangeDisplaySettings(dm, 0)
                    break

            except (self.exceptions):
                pass
            
        self.reset()

    def reset(self):
        reset = False
        while True:
            try:
                sleep(self.delay)
                hook = winhook().get_hook()

                if hook is None:
                    reset = True

                if reset:
                    ChangeDisplaySettings(None, 0)
                    break
            except (self.exceptions):
                pass

        self.apply()