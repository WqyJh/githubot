'''
Files management.

Usage: githubot file upload --token=TOKEN --repo=REPO  [FILES...]
       githubot file download --token=TOKEN --repo=REPO  [FILES...]
       githubot file delete --token=TOKEN --repo=REPO  [FILES...]

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


def get_contents(repo, filename):
    try:
        return repo.get_contents(filename)
    except Exception:
        pass


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


def delete_single(repo, content):
    repo.delete_file(content.path, 'Deleted by githubot', content.sha)


def delete_file(repo, filename):
    contents = get_contents(repo, filename)

    if not contents:
        print('{} does not exist'.format(filename))
        return

    # single file
    if not isinstance(contents, Sequence):
        delete_single(repo, contents)
        return

    # a set of files
    while contents:
        file_content = contents.pop(0)
        if file_content.type == 'dir':
            contents.extend(repo.get_contents(file_content.path))
        else:
            delete_single(repo, file_content)


def delete_files(repo, files):
    for f in files:
        delete_file(repo, f)


def main():
    args = docopt(__doc__)

    token = args['--token']
    repo = args['--repo']
    files = args['FILES']

    g = Github(token)
    repo = g.get_repo(repo)

    if args['download']:
        download_files(repo, files)
    elif args['upload']:
        upload_files(repo, files)
    elif args['delete']:
        delete_files(repo, files)


if __name__ == '__main__':
    main()
