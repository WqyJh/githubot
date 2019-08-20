# githubot

[![Build Status](https://travis-ci.org/WqyJh/githubot.svg?branch=master)](https://travis-ci.org/WqyJh/githubot)
[![license](https://img.shields.io/badge/LICENCE-MIT-brightgreen.svg)](https://raw.githubusercontent.com/WqyJh/githubot/master/LICENSE)


Command line tool to use Github's API for automation:

- [x] create release with assets
- [ ] TODO

## Installation

```bash
pip install githubot
```

## Usage

```bash
Usage: run.py [OPTIONS] [ASSETS]...

Options:
  --token TEXT      Github access token  [required]
  -r, --repo TEXT   Repo full name like: <owner>/<repo>  [required]
  -t, --tag TEXT    Tag name for the release. If the tag does not
                    exist it will be created on default branch.  [required]
  --title TEXT      Title for the release
  --message TEXT    Message for the release
  --assets PATH...  Files to be uploaded as assets.
  --help            Show this message and exit.
```

For example:

```bash
githubot \
--token <my_github_token> \
--repo Wqyjh/test \
-t test_tag \
--title "This is an test title" \
--message "This release contains xxx" \
--assets assets/*
```

Only regular files are supported for the `--assets` option, directories are not supported.
You can specify files in the following manner:

```bash
--assets file1 file2
--assets path/*
```