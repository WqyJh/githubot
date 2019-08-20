'''
File management.

Usage: githubot file upload --token=TOKEN --repo=REPO  [FILES...]
       githubot file download --token=TOKEN --repo=REPO  [FILES...]

Options:
    --token=TOKEN           Github access token.
    -r=REPO --repo=REPO     Repo full name like: owner/repo.
    -h --help               Show this message and exit.
'''

import os
import base64

from docopt import docopt
from github import Github


def download_file(repo, filename):
    contents = repo.get_contents(filename)

    # TODO: check if the path is an absolute path
    # if so, then convert it to relative.
    base = os.path.dirname(contents.path)
    if base:
        os.makedirs(base, exist_ok=True)

    with open(contents.path, 'wb') as f:
        f.write(base64.b64decode(contents.content))


def download_files(repo, files):
    for f in files:
        download_file(repo, f)


def file(token, repo, files):
    g = Github(token)
    repo = g.get_repo(repo)
    download_files(repo, files)


def main():
    args = docopt(__doc__)

    token = args['--token']
    repo = args['--repo']
    files = args['FILES']

    file(token, repo, files)


if __name__ == '__main__':
    download_file()