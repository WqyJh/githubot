'''
Command line tool to use Github's API for automation.

Usage: githubot [--version] <command> [<args>...]

options:
    -h --help   Show this message and exit.
    -v --version   Show version.

Subcommand:

config      Config management.
release     Releases management.
file        Files management.
'''

import sys
import runpy

from docopt import docopt

from githubot import __version__
from githubot import release, config


def set_default_args():
    token = None
    repo = None
    for i, v in enumerate(sys.argv):
        if '--token' in v:
            token = (i, v)
        if '--repo' in v:
            repo = (i, v)
    cfg = config.read_config()
    if not token:
        sys.argv.append(f'--token={cfg["token"]}')
    if not repo:
        sys.argv.append(f'--repo={cfg["repo"]}')

def main():
    args = docopt(__doc__, version=__version__, options_first=True)
    set_default_args()

    if args['<command>'] == 'release':
        from githubot import release
        release.main()
    elif args['<command>'] == 'file':
        from githubot import file
        file.main()
    elif args['<command>'] == 'config':
        from githubot import config
        config.main()
    else:
        pass


if __name__ == '__main__':
    main()
