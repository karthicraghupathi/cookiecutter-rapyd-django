# AGENTS.md

Conventions for AI coding agents and human contributors working in this project.

## Toolchain

- **uv** — the only package manager. Don't use pip, pipenv, or poetry.
- **ruff** — lint + format. Don't add black, isort, or flake8.
- **pre-commit** — hook orchestrator; runs ruff + standard hygiene checks +
  `uv-lock` / `uv-export` on every commit.
- **pytest** — test runner.

## Layout

```
{{ cookiecutter.project_slug }}/   Django project root (manage.py lives here)
{{ cookiecutter.project_slug }}/config/
    settings.py  — all env reads + logging config
    urls.py      — root URL conf (admin only by default; add your app URLs here)
    wsgi.py / asgi.py
tests/           — pytest tests
pyproject.toml   — single source of truth for deps + tool config
uv.lock          — exact pinned versions; committed
requirements.txt          — auto-generated (prod deps only); don't edit by hand
requirements-dev.txt      — auto-generated (prod + dev); don't edit by hand
.env             — local secrets; not committed
.env.example     — documents all required environment variables
```

## Adding a dependency

```bash
uv add <package>           # runtime dep → pyproject.toml + uv.lock
uv add --dev <package>     # dev-only dep
```

On the next commit, `uv-export` pre-commit hooks regenerate `requirements.txt` and
`requirements-dev.txt` automatically. Don't edit those files by hand.

## Django conventions

- **Custom user model**: `AUTH_USER_MODEL = "modernauth.User"`. Always import the user
  model via `django.contrib.auth.get_user_model()` in your own apps — never reference
  `modernauth.User` directly.
- **Settings**: all environment reads go through `environs.Env()` in
  `config/settings.py`. Don't add bare `os.environ` calls elsewhere.
- **Database**: defaults to SQLite via `DATABASE_URL` in `.env`. Update that value for
  PostgreSQL or another backend; no code changes needed.
- **New apps**: create under the project root, add to `INSTALLED_APPS`, run
  `uv run python {{ cookiecutter.project_slug }}/manage.py migrate`.

## Verification commands

After any change:

```bash
uv run python {{ cookiecutter.project_slug }}/manage.py check   # Django system check
uv run pytest
uv run ruff check .
uv run pre-commit run --all-files
```
