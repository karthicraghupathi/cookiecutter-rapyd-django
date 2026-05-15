# Cookiecutter Rapyd Django

[![Tests](https://github.com/karthicraghupathi/cookiecutter-rapyd-django/actions/workflows/test.yml/badge.svg)](https://github.com/karthicraghupathi/cookiecutter-rapyd-django/actions/workflows/test.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](#supported-python-versions)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template for Django projects.

## Quickstart

```bash
uvx cookiecutter gh:karthicraghupathi/cookiecutter-rapyd-django
```

You'll be prompted for project name, Python version, author name, and email. The
post-generation hook bootstraps the new project: `git init`, `uv sync`, pre-commit
install, and a one-shot `pre-commit run --all-files` to format the fresh files.

## What you get

A new Django project pre-configured with:

- **uv** for dependency management (single source of truth: `pyproject.toml`).
- **Django 4.2 LTS** with `environs`-based settings — `SECRET_KEY`, `DEBUG`,
  `ALLOWED_HOSTS`, and `DATABASE_URL` all read from `.env`. A random `SECRET_KEY`
  is generated automatically on first setup.
- **`modernauth`** — a custom `User` model with email as the username field
  (`AUTH_USER_MODEL = "modernauth.User"`).
- **ruff** for lint + format (replaces black + isort + flake8).
- **pre-commit** wired up with ruff hooks, standard hygiene hooks, and
  `uv-lock` / `uv-export` so committed `requirements.txt` and `requirements-dev.txt`
  stay in sync with `uv.lock`.
- **Logging** pre-configured: console handler + global `sys.excepthook` so uncaught
  exceptions are always logged before exit.
- **Supervisor + Gunicorn** deploy configuration (`supervisor.conf`, `gunicorn_start`).
- A `tests/` directory with one passing smoke test.
- A `Makefile` with `install`, `lint`, `format`, `test`, and `supervisor` targets.
- An `AGENTS.md` so AI coding agents understand the project conventions.

## Supported Python versions

3.10, 3.11, 3.12 (choose at generation time). Django 4.2 LTS supports all three.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — see [LICENSE](LICENSE).
