# Changelog

All notable changes to this project will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Pre-generation hook (`hooks/pre_gen_project.py`) that fails fast on an invalid
  `project_slug` (non-identifier or Python keyword), TOML-unsafe characters in
  project/author fields, and malformed `author_email`.
- Cookiecutter prompts: `python_version` (choice list: 3.12, 3.10, 3.11; default 3.12),
  `author_name`, `author_email`.
- `AGENTS.md` at repo root and inside generated projects documenting conventions for
  AI coding agents and human contributors.
- `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`, and `README.md` (uppercase).
- `.editorconfig` in both the template repo and generated projects.
- `.gitignore` at repo root (was missing entirely).
- Generated `.env.example` documenting all required environment variables.
- Generated `tests/` directory with `tests/__init__.py` and `tests/test_smoke.py`.
- Test suite expanded from 1 to 22 tests: file-manifest checks, variable rendering,
  ruff + pytest quality gates on the generated project, requirements-file content
  assertions, post-gen hook graceful failure when `uv` is absent, and pre-gen hook
  validation (invalid slug, Python keyword slug, unsafe chars, malformed email,
  non-ASCII author accepted).

### Changed

- **Replaced pipenv with uv** in both the template repo and generated projects.
  `Pipfile` / `Pipfile.lock` replaced by `pyproject.toml` + `uv.lock`.
- **Replaced black + isort + flake8 with ruff** in both layers. Configs consolidated
  into `[tool.ruff]` in `pyproject.toml`; separate `.flake8` and `.isort.cfg` files
  removed.
- Generated `pyproject.toml` is now a proper PEP 621 file — independent of the root
  (no longer a symlink) with `[project]`, `[dependency-groups]`, `[tool.ruff]`,
  `[tool.ruff.lint.isort]`, and `[tool.pytest.ini_options]`.
- Post-generation hook ported from bash (`post_gen_project.sh`) to Python
  (`post_gen_project.py`; cross-platform). Generates a random `DJANGO_SECRET_KEY`
  via `secrets.token_urlsafe()` instead of `/dev/urandom | base64`.
- Generated `.pre-commit-config.yaml` is now an independent file (no longer a symlink
  to the root). Uses ruff-pre-commit + uv-pre-commit (`uv-lock` + `uv-export` hooks).
- `readme.md` renamed to `README.md` in both layers.
- Generated `Makefile` modernised: `install`, `lint`, `format`, `test` targets via
  `uv run`; `supervisor` deploy target retained.
- `gunicorn_start` updated: venv path `../venv/` → `../.venv/` (uv default).
- `pre-commit-hooks` upgraded from v4.5.0 → v6.0.0.
- Root `.pre-commit-config.yaml` exclude pattern updated to skip the template
  directory (Jinja tokens would break the linter), replacing the old per-extension
  excludes.

### Removed

- `Pipfile`, `Pipfile.lock`, `requirements.txt`, `requirements-dev.txt`, `.flake8`,
  `.isort.cfg` at repo root.
- Generated `Pipfile`, `setup_env.sh`, `.flake8`, `.isort.cfg`, `requirements.txt`
  (replaced by auto-generated output from `uv-export` pre-commit hook).
- The custom `pipenv-requirements-pre-commit` hook (replaced by
  `astral-sh/uv-pre-commit` `uv-export`).
- The symlinks in the generated project for `.pre-commit-config.yaml`, `pyproject.toml`,
  `.flake8`, `.isort.cfg` — all replaced with independent files.
