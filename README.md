# githubot

[![Build Status](https://travis-ci.org/WqyJh/githubot.svg?branch=master)](https://travis-ci.org/WqyJh/githubot)
[![license](https://img.shields.io/badge/LICENCE-MIT-brightgreen.svg)](https://raw.githubusercontent.com/WqyJh/githubot/master/LICENSE)


Command line tool to use Github's API for automation:

- [x] create release with assets
- [x] upload/download files to github
- [ ] TODO

## Installation

```bash
pip install githubot
```

## Usage

### Create release with assets

```bash
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
```

For example:

Create a release to repo `WqyJh/test` with assets under the path of `assets/`.

```bash
githubot release --token <github_token> --repo WqyJh/test assets/*
```

Create a release and specify `tag`, `title` and `message` for it.

```bash
githubot release \
--token <github_token> \
--repo WqyJh/test \
--tag test_tag \
--title "This is an test title" \
--message "This release contains xxx" \
assets/*
```

Only regular files are supported for the `--assets` option, directories are not supported.
You can specify files in the following manner:

```bash
--assets file1 file2
--assets path/* # wildcard
```

### Use github repo as cloud storage

```bash
Files management.

Usage: githubot file upload --token=TOKEN --repo=REPO  [FILES...]
       githubot file download --token=TOKEN --repo=REPO  [FILES...]

Options:
    --token=TOKEN           Github access token.
    -r=REPO --repo=REPO     Repo full name like: owner/repo.
    -h --help               Show this message and exit.
```

#### Upload files

Upload files to github repo `WqyJh/test`.

```bash
./run.py file upload \
--token <github_token> \
--repo WqyJh/test \
file1 file2 file*
```

**Note** that the `FILES` argument is just the same with `ASSETS`, only regular files are supported.


#### Download files

Download files from github repo `WqyJh/test`.

```bash
./run.py file download \
--token <github_token> \
--repo WqyJh/test \
file1 dir1 dir2/
```

**Note** that the `FILES` argument here cannot contains wildcard, but it can contains directories.


#### Delete files

Delete files from github repo.

```bash
./run.py file delete \
--token <github_token> \
--repo Wqyjh/test \
file1 dir1 dir2/
```


## Development

- bumping 0.3.0 (PYPI)
- auto-changelog 1.15.0 (NPM)

The release processing is as follow:

1. Calculate semantic version
    ```bash
    git checkout dev
    git pull origin dev
    bumping
    ```
2. Create release branch from dev
    ```bash
    git checkout -b release-<version>
    ```
3. Modify the version and commit
4. Generate changelog and commit
    ```bash
    auto-changelog --latest-version <version>
    ```
5. Merge to master branch
6. Tag version to master branch
