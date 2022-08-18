import os
import sys
from argparse import ArgumentParser
from traceback import format_exc

from win32api import MessageBox

from execute import parse_n_run

if os.path.splitext(__file__)[1] == '.py':
    sys.path.append(os.path.dirname(__file__))


def main():
    parser = ArgumentParser()
    parser.add_argument('--executable', '-e', help='Executable to run.',
                        required=True, nargs=1, type=str)

    parser.add_argument('--priority', '-p', help='Set the process priority of the specified executable.',
                        default=None, nargs=1, type=str)

    parser.add_argument('--displaymode', '-dm',
                        help='Set the display mode for the specified executable.',
                        default=None, nargs=1, type=str)
    parse_n_run(parser.parse_args())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        MessageBox(None, format_exc(), str(e), 0)
        os._exit(1)
