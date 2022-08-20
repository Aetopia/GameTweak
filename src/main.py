from time import sleep
from traceback import format_exc
from handlers import display_mode, priority
from win32api import MessageBoxEx
import threading as td
from sys import argv
from os import chdir, path, _exit

def main():
    chdir(path.dirname(argv[0]))
    if path.exists('config.ini') is False:
        with open('config.ini', 'w') as config:
            config.write('''[Profiles]
; Application.exe/Title = Priority, Resolution
; Resolution -> 0x0
; Priority -> Normal, High, Above Normal
; App.exe = High, 1280x720
''')
    threads()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        _exit(0)
    

def threads():
    handlers = [display_mode.handler(), priority.handler()]

    for handler in handlers:
        td.Thread(target=handler.apply).start()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        MessageBoxEx(0, format_exc(), f'Error: {str(e)}', 0)
        _exit(0)
    