# Cookiecutter Rapyd Django

[Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/) template for a Django project.

## Features

- Requires Python 3.6
- Targets Django 3.2 LTS using version pinning.
- Requirements are managed using [Pipenv](https://pipenv.pypa.io/en/latest/).
- Uses [pre-commit](https://pre-commit.com/) to enforce coding standards. The following hooks are enabled with sane defaults for configurations:
  - [black](https://black.readthedocs.io/en/stable/) for formatting code.
  - [isort](https://pycqa.github.io/isort/) for organizing imports.
  - [flake8](https://flake8.pycqa.org/en/latest/) for linting code.
  - [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks) hooks for
    - `check-added-large-files` to prevent giant files from being committed.
    - `check-json` to load all json files to verify syntax.
    - `check-merge-conflict` to check for files that contain merge conflict strings.
    - `check-symlinks` to check for symlinks which do not point to anything.
    - `check-yaml` to load all yaml files to verify syntax.
    - `end-of-file-fixer` to make sure files end in a newline and only a newline.
    - `trailing-whitespace` to trim trailing whitespace.
- The `src` folder where your code will live contains the following:
  - A `settings.py` that
    - defines some important variables.
    - setups a good starting logging configuration along with an unhandled exception handler.
