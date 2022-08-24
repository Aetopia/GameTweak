from time import sleep
from handlers import display_mode, priority
import threading as td
from sys import argv
from os import chdir, path, _exit
from utils import error_handler

def main():
    chdir(path.dirname(argv[0]))
    if path.exists('GameTweak.ini') is False:
        with open('GameTweak.ini', 'w') as config:
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
        td.Thread(target=handler.thread).start()

if __name__ == '__main__':
    error_handler(main)
    