# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Setup

```bash
uv sync                              # install all dependencies into .venv
uv run python {{ cookiecutter.project_slug }}/manage.py migrate
uv run python {{ cookiecutter.project_slug }}/manage.py createsuperuser
uv run python {{ cookiecutter.project_slug }}/manage.py runserver
```

## Environment variables

Copy `.env.example` to `.env` and fill in the values (this is done automatically
on first setup):

| Variable | Default | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | *(generated)* | Django secret key — never commit a real value |
| `DEBUG` | `True` | Set to `False` in production |
| `ALLOWED_HOSTS` | *(empty)* | Comma-separated hostnames for production |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database connection URL |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

## Development commands

```bash
make install   # uv sync --all-groups
make lint      # ruff check .
make format    # ruff format .
make test      # uv run pytest
```

## Deployment

This project ships with a Supervisor + Gunicorn setup:

```bash
make supervisor   # installs supervisor.conf into /etc/supervisor/conf.d/
```

See `gunicorn_start` for tunable settings (workers, socket path, timeout).
