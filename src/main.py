import os
import sys
from argparse import ArgumentParser
from traceback import format_exc

from win32api import MessageBox

from execute import parse_n_run

if os.path.splitext(__file__)[1] == '.py':
    sys.path.append(os.path.dirname(__file__))

version = '0.0.0.1'


def main():
    parser = ArgumentParser(add_help=False)
    parser.add_argument('--executable', '-e', required=True, nargs=1, type=str)

    parser.add_argument('--priority', '-p', default=None, nargs=1, type=str)

    parser.add_argument('--displaymode', '-dm',
                        default=None, nargs=1, type=str)

    if len(sys.argv) == 1:
        MessageBox(None, '''Usage:
gametweak.exe --executable, -e <Executable> [options]

Options:
--priority  [high | above_normal]
--displaymode  <Display Mode>
''', f'GameTweak {version}', 0)
        return

    parse_n_run(parser.parse_args())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        MessageBox(None, format_exc(), str(e), 0)
        os._exit(1)
