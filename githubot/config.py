'''
Config management.

Usage: githubot config --token=TOKEN --repo=REPO

Options:
    --token=TOKEN           Github access token.
    -r=REPO --repo=REPO     Repo full name like: owner/repo.
    -h --help               Show this message and exit.
'''

import os
import json

HOME = os.path.join(os.environ['HOME'], '.githubot')
CONFIG = os.path.join(HOME, 'config.json')

config = None

from docopt import docopt

def save_config(token, repo):
    if not os.path.isdir(HOME):
        os.makedirs(HOME, mode=0o700, exist_ok=True)
    with open(CONFIG, 'w') as f:
        json.dump({'token': token, 'repo': repo}, f, indent=4)

def read_config():
    with open(CONFIG, 'r') as f:
        global config
        config = json.load(f)
        return config

def main():
    args = docopt(__doc__)

    token = args['--token']
    repo = args['--repo']

    save_config(token, repo)

if __name__ == '__main__':
    main()
