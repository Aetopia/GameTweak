import os
import sys
from argparse import ArgumentParser
from traceback import format_exc

from win32api import MessageBox

from execute import parse_n_run

if os.path.splitext(__file__)[1] == '.py':
    sys.path.append(os.path.dirname(__file__))

version = '0.0.2'


def main():
    parser = ArgumentParser(add_help=False)
    parser.add_argument('--executable', '-e', required=True, type=str)

    parser.add_argument('--priority', '-p', default=None, type=str)

    parser.add_argument('--displaymode', '-dm',
                        default=None, nargs=1, type=str)
    
    parser.add_argument('--launcher', '-l', action='store_true')

    if len(sys.argv) == 1:
        MessageBox(None, '''Usage:
gametweak.exe --executable, -e <Executable> [options]

Options:
--priority > Process Priority [high | above_normal]
--displaymode > Display Resolution [Display Mode]
--launcher > Launcher Support''', f'GameTweak {version}', 0)
        return

    parse_n_run(parser.parse_args())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        MessageBox(None, format_exc(), str(e), 0)
        os._exit(1)
    except KeyboardInterrupt:
        os._exit(0)
