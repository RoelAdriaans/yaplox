# YaPlox - Yet Another Python implementation for Lox

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project is a python implementation for Lox. Read more at <https://craftinginterpreters.com>

## Structure

Since we're implementing this in Python, the structure will be a little bit different.
For example, the main class is called Yaplox, and not Lox as in the original implementation.

### Files

- `lox/Lox.java` is called `yaplox/yaplox.py`

## Poetry

This project uses `poetry` to manage dependencies. Some commands:

### Add dependency

Add a new package to the dependencies use:

```shell
poetry add <Package>
```

To add it a a development dependency use:

```shell
poetry add -D <package>
```

### Install project

Install the project with the command

```shell
poetry install
```

### Other usefull commands

Update packages:

```shell
poetry update
```

Show installed packages:

```shell
poetry show --tree
```

It's possible to add `-D` to hide the development dependencies.
