'''
Files management.

Usage: githubot file upload --token=TOKEN --repo=REPO  [FILES...]
       githubot file download --token=TOKEN --repo=REPO  [FILES...]

Options:
    --token=TOKEN           Github access token.
    -r=REPO --repo=REPO     Repo full name like: owner/repo.
    -h --help               Show this message and exit.
'''

import os
import base64

from typing import Sequence

from docopt import docopt
from github import Github


def download_contents(contents):
    # TODO: check if the path is an absolute path
    # if so, then convert it to relative.
    base = os.path.dirname(contents.path)
    if base:
        os.makedirs(base, exist_ok=True)

    with open(contents.path, 'wb') as f:
        f.write(base64.b64decode(contents.content))


def download_file(repo, filename):
    contents = repo.get_contents(filename)

    # single file
    if not isinstance(contents, Sequence):
        download_contents(contents)
        return

    # a set of files
    while contents:
        file_content = contents.pop(0)
        if file_content.type == 'dir':
            contents.extend(repo.get_contents(file_content.path))
        else:
            print(file_content)
            download_contents(file_content)


def download_files(repo, files):
    for f in files:
        download_file(repo, f)


def upload_file(repo, filename):
    try:
        contents = repo.get_contents(filename)
    except Exception:
        contents = None

    with open(filename, 'rb') as f:
        file_content = f.read()

    if contents:
        repo.update_file(contents.path, 'Updated by githubot', file_content,
                         contents.sha)
    else:
        repo.create_file(filename, 'Uploaded by githubot', file_content)


def upload_files(repo, files):
    for f in files:
        upload_file(repo, f)


def file(token, repo, files, download=True):
    g = Github(token)
    repo = g.get_repo(repo)

    if download:
        download_files(repo, files)
    else:
        upload_files(repo, files)


def main():
    args = docopt(__doc__)

    token = args['--token']
    repo = args['--repo']
    files = args['FILES']
    download = args['download']

    file(token, repo, files, download=download)


if __name__ == '__main__':
    main()
