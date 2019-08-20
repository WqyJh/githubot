'''
Command line tool to use Github's API for automation.

Usage: githubot [--version] <command> [<args>...]

options:
    -h --help   Show this message and exit.
    -v --version   Show version.

Subcommand:

release     Releases management.
file        Files management.
'''

import runpy

from docopt import docopt

from githubot import __version__
from githubot import release

if __name__ == '__main__':
    args = docopt(__doc__, version=__version__, options_first=True)

    if args['<command>'] == 'release':
        from githubot import release
        release.main()
    elif args['<command>'] == 'file':
        from githubot import file
        file.main()
    else:
        pass
