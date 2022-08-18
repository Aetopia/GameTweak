from argparse import ArgumentParser
from execute import parse_n_run
import sys
import os
from traceback import format_exc, print_exc
from win32api import MessageBox
if os.path.splitext(__file__) == '.py':
    sys.path.append(os.path.dirname(__file__))


def main():
    parser = ArgumentParser()
    parser.add_argument('-e')
    parser.add_argument('-p')
    parser.add_argument('-dm')
    parse_n_run(parser.parse_args())


if __name__ == '__main__':
    try:
        main()
    except:
        MessageBox(None, format_exc(), 'Error', 0)
        
