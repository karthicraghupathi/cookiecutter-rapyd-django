# Contributing

Thanks for your interest in this template.

## Dev setup

```bash
git clone <fork-url>
cd cookiecutter-rapyd-django
uv sync                              # creates .venv from pyproject.toml + uv.lock
uv run pre-commit install            # registers the git pre-commit hook
```

## Running tests

```bash
uv run pytest
```

Tests bake the template into a temp directory and assert the generated project lints
and passes its own test suite. The first run downloads Django and other packages from
PyPI; subsequent runs use uv's local cache and are much faster.

## Adding a cookiecutter prompt

1. Add the key to `cookiecutter.json` (use a list for choices; first item is the default).
2. Reference it in template files via `{{ cookiecutter.<key> }}`.
3. If the new value needs validation, add a check in `hooks/pre_gen_project.py`.
4. If the prompt affects post-generation setup, update `hooks/post_gen_project.py`.
5. Add a test in `test_cookiecutter.py` that bakes with the new value and asserts the
   rendered output.

## Release process

1. Update `CHANGELOG.md` with the new version section.
2. Bump `version` in `pyproject.toml` (`[project].version`).
3. Commit, then tag: `git tag v<version> && git push --tags`.

## Code style

ruff handles lint + format. Pre-commit runs both on every commit. If pre-commit fails,
run these locally first:

```bash
uv run ruff check --fix .
uv run ruff format .
```

Note: mypy is configured in the *generated* project, not in this template repo
(the hook files contain Jinja tokens that make them non-importable). Run
`uv run mypy .` inside a baked project, not here.
