import click

from typing import Sequence
from github import Github

from githubot import __version__


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def create_release(repo, tag, title, message, assets: Sequence[str]):
    # Draft a release
    release = repo.create_git_release(tag, title, message)

    if assets:
        # Uploading assets
        for asset in assets:
            release.upload_asset(asset)

    # Confirm the draft
    release.update_release(title, message, draft=False)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--token', required=True, help='Github access token')
@click.option('-r', '--repo', required=True,
              help='Repo full name like: <owner>/<repo>')
@click.option('-t', '--tag', required=True,
              help='Tag name for the release. If the tag does not \
                exist it will be created on default branch.')
@click.option('--title', default='Released by githubot.',
              help='Title for the release')
@click.option('--message', default='', help='Message for the release')
@click.option('--assets', nargs=0, type=click.Path(exists=True),
              help='Files to be uploaded as assets.')
@click.argument('assets', nargs=-1)
@click.version_option(version=__version__)
def main(token, repo, tag, title, message, assets: Sequence[str]):
    g = Github(token)
    repo = g.get_repo(repo)
    create_release(repo, tag, title, message, assets)


if __name__ == '__main__':
    main()
