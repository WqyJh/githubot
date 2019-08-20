'''
Releases management.

Usage: githubot release --token=TOKEN --repo=REPO
                        [--tag=TAG] [--title=TITLE] [--message=MESSAGE]
                        [ASSETS...]

Options:
    --token=TOKEN           Github access token.
    -r=REPO --repo=REPO     Repo full name like: owner/repo.
    --tag=TAG               Tag name for the release. If the tag does not
                            exist it will be created on default branch.
    --title=TITLE           Title for the release.
    --message=MESSAGE       Message for the release.
    -h --help               Show this message and exit.
'''

from docopt import docopt
from github import Github
from typing import Sequence

from datetime import datetime


def create_release(repo, tag, title, message, assets: Sequence[str]):
    # Draft a release
    release = repo.create_git_release(tag, title, message)

    if assets:
        # Uploading assets
        for asset in assets:
            release.upload_asset(asset)

    # Confirm the draft
    release.update_release(title, message, draft=False)


def release(token, repo, tag, title, message, assets: Sequence[str]):
    g = Github(token)
    repo = g.get_repo(repo)
    create_release(repo, tag, title, message, assets)


def main():
    args = docopt(__doc__)

    now = datetime.today().strftime('%Y%m%d-%H%M%S')

    token = args['--token']
    repo = args['--repo']
    tag = args['--tag'] or 'untagged-{}'.format(now)
    title = args['--title'] or tag
    message = args['--message'] or 'Rselease created by githubot.'
    assets = args['ASSETS']

    release(token, repo, tag, title, message, assets)


if __name__ == '__main__':
    main()
