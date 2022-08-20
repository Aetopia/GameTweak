from win32gui import GetForegroundWindow, GetWindowText
from win32process import GetWindowThreadProcessId
from psutil import Process
from configparser import ConfigParser
from os import path

class winhook:
    def __init__(self) -> None:
          pass

    def hook_process(self) -> tuple[str, str, int]:
        """
        Get the title, full path to the executable & PID of the active process.
        """
        hwnd = GetForegroundWindow()
        pid = GetWindowThreadProcessId(hwnd)[1]
        title = GetWindowText(hwnd)
        return title, path.split(Process(pid).exe())[1], pid

    def get_hook(self) -> str:
        config = ConfigParser()
        config.read('config.ini')

        title, exe, _ = self.hook_process()
        profiles = config['Profiles']

        if exe == 'applicationframehost.exe':
            if title in profiles:
                return config['Profiles'][title]

        elif exe in profiles:
            return config['Profiles'][exe]

        else:
            return None
