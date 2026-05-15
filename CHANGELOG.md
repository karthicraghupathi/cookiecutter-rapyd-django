# Changelog

All notable changes to this project will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [1.0.0] - 2026-05-15

### Added

- Pre-generation hook (`hooks/pre_gen_project.py`) that fails fast on an invalid
  `project_slug` (non-identifier, non-ASCII, or Python keyword), TOML-unsafe
  characters in project/author fields, and malformed `author_email`.
- Cookiecutter prompts: `python_version` (choice list: 3.12, 3.10, 3.11; default 3.12),
  `author_name`, `author_email`.
- `AGENTS.md` at repo root and inside generated projects documenting conventions for
  AI coding agents and human contributors.
- `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`, and `README.md` (uppercase).
- `.editorconfig` in both the template repo and generated projects.
- `.gitignore` at repo root (was missing entirely); entries for `.idea/`, `.vscode/`,
  `.mypy_cache/`, and standard Python build artefacts.
- `.vscode/settings.json` removed from version control (now gitignored).
- Generated `.env.example` documenting all required environment variables.
- Generated `tests/` directory with `tests/__init__.py` and `tests/test_smoke.py`.
- **mypy + django-stubs** in the generated project (moderate strictness: django-stubs
  plugin, `check_untyped_defs`, `ignore_missing_imports`, `mypy_path` scoped to the
  Django app directory). `[tool.mypy]` and `[tool.django-stubs]` sections added to
  the generated `pyproject.toml`.
- Local mypy pre-commit hook in the generated project (`uv run mypy .`, `language:
  system`) so the django-stubs plugin can import Django from the project's own venv.
- `.github/workflows/test.yml` in the template repo: lint job (ruff check + ruff
  format) and test job (Python-version matrix from `cookiecutter.json`, concurrency
  cancellation).
- `.github/workflows/test.yml` generated inside each new project: single-version
  matrix driven by `{{ cookiecutter.python_version }}`; GitHub `${{ }}` expressions
  protected by `{% raw %}` blocks so Jinja rendering leaves them intact.
- `.github/workflows/release.yml`: auto-creates a GitHub Release with generated
  release notes on any `v*` tag push.
- `.github/dependabot.yml`: monthly Dependabot updates for `pip`, `github-actions`,
  and `pre-commit` ecosystems.
- Test suite covering: default bake success, file manifest (expected + generated +
  obsolete), custom slug rendering, `python_version` in pyproject + CI matrix,
  author rendering, `.env` secret key, modernauth integration, ruff/pytest/mypy
  quality gates on the generated project, requirements-file content, post-gen hook
  graceful failure when `uv` is absent, no repo-local git identity in scaffold commit,
  CI-workflow verbatim copying, pre-gen input validation (invalid slug, Python keyword,
  non-ASCII slug, unsafe chars in name/author, invalid/quoted email, non-ASCII author
  accepted). **26 tests** total.

### Changed

- **Replaced pipenv with uv** in both the template repo and generated projects.
  `Pipfile` / `Pipfile.lock` replaced by `pyproject.toml` + `uv.lock`.
- **Replaced black + isort + flake8 with ruff** in both layers. Configs consolidated
  into `[tool.ruff]` in `pyproject.toml`; separate `.flake8` and `.isort.cfg` files
  removed.
- Generated `pyproject.toml` is now a proper PEP 621 file — independent of the root
  (no longer a symlink) with `[project]`, `[dependency-groups]`, `[tool.ruff]`,
  `[tool.ruff.lint.isort]`, `[tool.pytest.ini_options]`, `[tool.mypy]`, and
  `[tool.django-stubs]`.
- Post-generation hook ported from bash (`post_gen_project.sh`) to Python
  (`post_gen_project.py`; cross-platform). Generates a random `DJANGO_SECRET_KEY`
  via `secrets.token_urlsafe()` instead of `/dev/urandom | base64`. Now verifies
  critical generated files (`uv.lock`, `requirements.txt`, `requirements-dev.txt`)
  are non-empty before the scaffold commit.
- Generated `.pre-commit-config.yaml` is now an independent file (no longer a
  symlink). Uses ruff-pre-commit + local mypy hook + uv-pre-commit (`uv-lock` +
  `uv-export` hooks). Hook versions: `pre-commit-hooks` v6.0.0, `ruff-pre-commit`
  v0.15.13, `uv-pre-commit` 0.11.14.
- Generated `config/settings.py` made type-clean: `env.log_level` default changed
  from `"INFO"` (str) to `logging.INFO` (int) to satisfy the typed overload;
  `ALLOWED_HOSTS` annotated as `list[str]`.
- Generated `manage.py` `main()` annotated with `-> None`.
- `readme.md` renamed to `README.md` in both layers.
- Generated `Makefile` modernised: `install`, `lint`, `format`, `test` targets via
  `uv run`; `supervisor` deploy target retained.
- `gunicorn_start` updated: venv path `../venv/` → `../.venv/` (uv default).
- `pre-commit-hooks` upgraded from v4.5.0 → v6.0.0.
- Root `.pre-commit-config.yaml` exclude pattern updated to skip the template
  directory (Jinja tokens break linters), replacing the old per-extension excludes.
- All third-party GitHub Actions pinned to specific versions (`actions/checkout@v6.0.2`,
  `astral-sh/setup-uv@v8.1.0`).
- `_copy_without_render` cleared; GitHub `${{ }}` expressions in the inner CI
  workflow protected with `{% raw %}` blocks instead (allows `{{ cookiecutter.* }}`
  tokens to still render in the same file).

### Removed

- `Pipfile`, `Pipfile.lock`, `requirements.txt`, `requirements-dev.txt`, `.flake8`,
  `.isort.cfg` at repo root.
- Generated `Pipfile`, `setup_env.sh`, `.flake8`, `.isort.cfg`, `requirements.txt`
  (replaced by auto-generated output from `uv-export` pre-commit hook).
- The custom `pipenv-requirements-pre-commit` hook (replaced by
  `astral-sh/uv-pre-commit` `uv-export`).
- The symlinks in the generated project for `.pre-commit-config.yaml`, `pyproject.toml`,
  `.flake8`, `.isort.cfg` — all replaced with independent files.
- `.vscode/settings.json` removed from git tracking.
